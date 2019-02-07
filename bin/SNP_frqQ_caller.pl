package main;
use strict;
use Getopt::Long;
use IO::File;

my $cut_off_frq = 0.1;
my $cut_off_Q = 20;
my $indel_lower_limit = 10;
my $infile;
my $cut_off_num = 10;
my $mq_cutoff = 20;
my $cut_off_Q2 = 20;
my $cut_off_num2 = 2;
my $indel_allele_frq_cutoff = 0.1;
my $target_genotype;
my $indel_out_file;
my $SNV_out_file;

GetOptions(
		"Infile=s" => \$infile,
		"INDEL=s" => \$indel_out_file,
		"SNV=s" => \$SNV_out_file,
		"cut_off_frq=f" => \$cut_off_frq,
		"cut_off_num=i" => \$cut_off_num,
		"cut_off_Q=i" => \$cut_off_Q,
		"indel_allele_num_cutoff=i" => \$indel_lower_limit,
		"indel_allele_frq_cutoff=f" => \$indel_allele_frq_cutoff,
		"mq_cutoff=i" => \$mq_cutoff,
		"genotype=s" => \$target_genotype	
);

$cut_off_Q2 = $cut_off_Q;
$cut_off_num2 = $cut_off_num;

if(defined($infile) != 1){print"-Infile Input file!!!\n"; exit;}
if(defined($indel_out_file) != 1){print"-INDEL Indel output file!!!\n"; exit;}
if(defined($SNV_out_file) != 1){print"-SNV SNV output file!!!\n"; exit;}

open INDEL, ">$indel_out_file" or die "$indel_out_file!!"; 
open SNV, ">$SNV_out_file" or die "$SNV_out_file!!"; 

print SNV "#chr\tpos\tref\tgenotype\ttotal\tA\tT\tG\tC\tA\tT\tG\tC\n";
print INDEL "#chr\tpos\tref\tgenotype\ttotal\tnon_indel\tindel\tnon_indel\tindel\n";

my @SNP;
my $pos;
my $total = 0;
my $total_SNPs = 0;
my $total_ins = 0;
my $total_del = 0;
my $chr;
my $pre_depth;
my @neighbor_indel;
my @neighbor_low_cq;

# set base_quality conversion table
my %convert;
for ( 0..100 ){
	$convert{pack("C", $_+33)} = $_ ;
}

if($infile =~ /bz2$/){open IN_PILE, "bzcat $infile | " or die "$infile !!";}
else{open IN_PILE, "$infile" or die "$infile !!";}

my $num_error = 0;
my $total_cov = 0;
while(<IN_PILE>){
	if($_ =~ /^#/){next;}
	chomp;
	$total++;
	my @l = split("\t", $_);

#	if($l[0] ne $target_chr || $l[1] != $target_pos){next;}

	$chr = $l[0];
	$l[2] = uc($l[2]);
	my $ref = $l[2];

###################################

	my @mq;
	foreach( split("", $l[6]) ){ 
		die "Undefined mapping quality!!! $_\n" if( !defined $convert{$_} );
		$_ = $convert{$_};
		push( @mq, $_);
	}

	my @BQ = split("", $l[5]); 

	my ($base2, $indel) = &get_base_indel($l[0], $l[1], $l[2], $l[4]); #170509 $l[8] => $l[4] 
	my @base2 = @{$base2};
	my @indel = @{$indel};

	if( $#BQ != $#base2 || $#mq != $#base2 ){
		die join( ",",  "$l[0] $l[1] Diffrent number of #BQ, #base, #MQ :",$#BQ , $#base2 , $#mq ), "\n";
	}

###################################
	my @geno = &SNP_frq_Q(\@BQ, \@base2, \@mq, $ref, $cut_off_Q, $mq_cutoff, $cut_off_frq, $cut_off_num, $cut_off_Q2, $cut_off_num2);
	@geno = ($l[0], $l[1], $ref, @geno);

	my %count = ("A" => $geno[5], "T" => $geno[6], "G" => $geno[7], "C" => $geno[8]);
	
	my $k = 0;
	foreach(sort {$count{$b} <=> $count{$a}}  keys %count){
		if($k){$num_error += $count{$_};}
		$k++;
	}
	$total_cov += $geno[4];

	my $ref2 = "$ref"."$ref";

	if ($ref2 ne $geno[3] and $geno[3] ne "--"){	
		print SNV join("\t", @geno), "\n";
	}
#	print"num_error $num_error total_cov $total_cov\n";
#	next;
	my @indel_geno;
	if(@indel >= $indel_lower_limit){
		my %num_indel;
		foreach(@indel){$num_indel{$_}++;}
		my $indel_allele;
		my $indel_allele_num = 0;
		foreach(sort {$num_indel{$b} <=> $num_indel{$a}} keys %num_indel){
			if(! $indel_allele){
				$indel_allele_num = $num_indel{$_};
				$indel_allele = $_;
			}
		}
		my $ref_allele_num = $total_cov;
		if ($indel_allele =~ /^-/){
			$ref_allele_num = $l[3];
		}
		else{
			$ref_allele_num = $l[3] - $indel_allele_num;
		}
		@indel_geno = &indel_frq_Q($indel_allele, $ref_allele_num, $indel_allele_num, $ref, $indel_lower_limit, $indel_allele_frq_cutoff);
		if($indel_geno[0] ne "--"){
			@indel_geno = ($l[0], $l[1], $ref, @indel_geno);
			print INDEL join("\t", @indel_geno), "\n";
		}
	}
}
close(IN_PILE);

sub compare_genotype{
	my ($cancer, $normal) = @_;
	my @cancer = split("", $cancer);
	my @normal = split("", $normal);

	my %normal;
	foreach(@normal){$normal{$_} = 1;}

	my $cancer_specific_varinat = 0;
	foreach my $cancer_tmp (@cancer){
		if(exists($normal{$cancer_tmp}) == 0){$cancer_specific_varinat++;}
	}

	return $cancer_specific_varinat;
}

sub get_base_indel{
	my ($chr, $pos, $ref, $base) = @_;

	my (@base2, @indel);
	my $indel_character = 0;
	for(my $k = 0; $k < length($base); $k++){
		my $b = substr( $base, $k, 1);
		if( $b eq "+" || $b eq "-"){
			if( substr( $base, $k+1, length($base)) =~ /^(\d+)/ ){
				my $indel_len_num = $1;
				my $indel = substr($base, $k, length($indel_len_num) + $1 + 1);
				$indel = uc($indel);
				$indel =~ s/[0-9]//g;
				push(@indel, $indel);
				$indel_character += length($indel_len_num) + $indel_len_num + 1;
				$k += length($indel_len_num) + $indel_len_num;
				next;
			}
			else{die "????? $chr $pos $base\n";}
		}
		elsif( $b eq "^" ){$k++; next;}
		elsif( $b eq '$' ){next;}
		elsif($b eq "." || $b eq ","){push(@base2, $ref);}
		elsif($b =~ /[a-z,A-Z,\*]/){push( @base2, uc($b));}
		elsif( $b =~ /\d/ ){die "?? $chr $pos $base\n";}
		else{die "??? $chr $pos $base $b\n";}
	}

	return(\@base2, \@indel);
}

sub SNP_frq_Q{
	my( $BQ, $base2, $mq, $ref, $cut_off_Q, $mq_cutoff, $cut_off_frq, $cut_off_num, $cut_off_Q2, $cut_off_num2) = @_;

	my @BQ = @$BQ;
	my @base2 = @$base2;
	my @mq = @$mq;
	my %call;
	$call{A} = 0; $call{T} = 0; $call{G} = 0; $call{C} = 0;
	my %call2;
        $call2{A} = 0; $call2{T} = 0; $call2{G} = 0; $call2{C} = 0;

	for(my $j = 0; $j < @BQ; $j++){
		next if( $base2[$j] eq '*' );
		$_ = $convert{$BQ[$j]};
		if($_ >= $cut_off_Q && $mq[$j] >= $mq_cutoff){
				$call{$base2[$j]}++;
		}
		if($_ >= $cut_off_Q2 && $mq[$j] >= $mq_cutoff){                  
				$call2{$base2[$j]}++;
        }
	}

	my @allele;
	my $geno;

	my ($A, $T, $G, $C ) = ($call{A}, $call{T}, $call{G}, $call{C});
	my ($A2, $T2, $G2, $C2 ) = ($call2{A}, $call2{T}, $call2{G}, $call2{C});

	my $cov = $A + $T + $G + $C;

	if($cov == 0){
		$geno = "--";
		return ($geno, $cov, $A, $T, $G, $C, 0, 0, 0, 0, 0);
	}

	my %call_num = ("A" => $A, "T" => $T, "G" => $G, "C" => $C);
	my %call_num2 = ("A" => $A2, "T" => $T2, "G" => $G2, "C" => $C2);

	my @allele;
	foreach(keys %call_num){
		if(($call_num{$_}/$cov >= $cut_off_frq) and ($call_num{$_} >= $cut_off_num) and ($call_num2{$_} >= $cut_off_num2)){push(@allele, $_);}
	}

	my $geno = join("", sort(@allele));

	if($geno !~ /[A-Z]/){$geno = "--";}

	if(length($geno) == 1){$geno = "$geno"."$geno";}

	return ($geno, $cov, $A, $T, $G, $C, &round($A/$cov,10), &round($T/$cov,10), &round($G/$cov,10), &round($C/$cov,10));
}
sub indel_frq_Q{
	my($indel_allele, $ref_allele_num, $indel_allele_num, $ref, $indel_lower_limit, $indel_allele_frq_cutoff) = @_;
	my $cov = $indel_allele_num + $ref_allele_num;

	my $geno;
	my $ref_allele_frq = 0;
	my $indel_allele_frq = 0;
	$indel_allele_frq = &round($indel_allele_num/$cov, 10);
	$ref_allele_frq = &round($ref_allele_num/$cov, 10);
	if($indel_allele_frq >= $indel_allele_frq_cutoff && $indel_allele_num >= $indel_lower_limit){$geno = $indel_allele;}
	else{$geno = "--"}

	return ($geno, $cov, $ref_allele_num, $indel_allele_num, $ref_allele_frq, $indel_allele_frq);
}
sub round{
	my $A = shift;
	my $degit = shift;

	$A = int($A*(10**($degit - 1)) + 0.5)/(10**($degit - 1));
	return $A;
}
sub rev_con{
	my $base = shift;
	$base = uc($base);
	$base =~ tr/[ATGC]/[TACG]/;
	$base = reverse($base);
	return($base);
}


