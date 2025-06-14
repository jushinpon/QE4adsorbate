#!/usr/bin/perl
use strict;
use warnings;
use File::Basename;
use Cwd;
use Algorithm::Combinatorics qw(combinations_with_repetition);

my $currentPath = getcwd();# dir for all scripts

my $store_path = "$currentPath/data4QEinput";#store path
`rm -rf $store_path`;
`mkdir -p $store_path`;

my $dir = "$currentPath/data4adsorption";#source path of data files

my @datafile = `find $dir -type f -name "*.data"`;#
map { s/^\s+|\s+$//g; } @datafile;
die "No data files\n" unless(@datafile);

# --- CONFIGURATION ---
my $move_step = 3;  # 0..$move_step, the max step number for moving adsorbents
my $incre_z = 1.6;  # incremnt of z coordinate for each step
my @target_elements = ("Li");
my %is_target = map { $_ => 1 } @target_elements;


my @infiles = @datafile;  # List of input files to process
# --- MAPPING AND MAIN LOOP ---
foreach my $infile (@infiles) {
    my $prefix = basename($infile, ".data");
    my $outfile = "${prefix}_Zmoved.data";

    my %type_to_element;
    my %target_types;
    my @lines;
    my @atoms_data;
    my $in_atoms = 0;
    my $in_masses = 0;
    my $atoms_start = 0;
    my $typeNum = `grep "atom types" $infile|awk '{print \$1}'`;
    chomp  $typeNum;
    my @ele = `grep -v '^[[:space:]]*\$' $infile|grep -A $typeNum Masses|grep -v Masses|grep -v -- '--'|awk '{print \$NF}'`;
    #my @ele = `grep -v '^[[:space:]]*\$' $_|grep -A $typeNum Masses|grep -v Masses|grep -v -- '--'|awk '{print \$NF}'`;
    map { s/^\s+|\s+$//g; } @ele;
    die "No Masses for finding element symbol in $infile\n" unless(@ele);
    
    %target_types = map {
        $is_target{$ele[$_]} ? ($_ + 1 => $ele[$_]) : ()
    } 0..$#ele;
    
    die "No target elemets to move in $infile!\n" unless %target_types;  #if none of the target elements are present

    #keep the lines before Atoms section
    my @first_part = `grep -v Atomsk $infile|grep -B 500 Atoms|grep -v Atoms|grep -v -- '--'`;
    map { s/^\s+|\s+$//g; } @first_part;
    my $first_part = join("\n", @first_part);
    die "No Atoms section in $infile!\n" unless $first_part;#if no Atoms section, skip this file
    
    my $atomNum = `grep "atoms" $infile|awk '{print \$1}'`;
    $atomNum =~ s/^\s+|\s+$//g;#could no specific type in coords info
    
    my @coordinates = `grep -v '^[[:space:]]*\$' $infile|grep -v Atomsk|grep -A $atomNum Atoms|grep -v Atoms|grep -v -- '--'`;#get types
    map { s/^\s+|\s+$//g; } @coordinates;
    die "No coordinates for atoms in $infile!\n" unless(@coordinates);  
    
    my @other_z;
    my @modified_atoms;
    @lines = @coordinates;
#
    for (my $i = 0; $i < @lines; $i++) {#go through the coordinate lines
        my $line = $lines[$i];
        my @fields = split(/\s+/, $line);
        my ($id, $type, $x, $y, $z) = @fields;

        if (exists $target_types{$type}) {
            #id of @lines, atom id, type, x, y, z
            push @modified_atoms, [$i, $id, $type, $x, $y, $z];
        } else {
            push @other_z, $z;
        }
    }
    my $max_z = (sort { $b <=> $a } @other_z)[0];
    my $new_z_base = $max_z + 1.0;#just guess a new z coordinate
    my $modified_atoms_count = scalar @modified_atoms;# atom number to be modified (array length)
    my @domain = (0 .. $move_step);# value range for each atom to be moved
    my $iter = combinations_with_repetition(\@domain, $modified_atoms_count);
    my @all_combinations;
    while (my $combo = $iter->next) {
        push @all_combinations, [ map { $_ * $incre_z } @$combo ];
    }
    my $count = 0;
    for my $combo_ref (@all_combinations) {
        my @moveZ_vectors = @$combo_ref;#get the first element of the array
                
        for my $aid (0..$#modified_atoms){#array reference
            my ($line_index, $id, $type, $x, $y, $z) = @{$modified_atoms[$aid]};
            my $new_z = $new_z_base + $moveZ_vectors[$aid];
            my $temp = join(' ', $id, $type, $x, $y, $new_z);#lmp format
            $lines[$line_index] = $temp;#update the line in the array
        }
        my $second_part = join("\n", @lines);
        my %heredoc_hr = (
            first_part => $first_part,
            second_part => $second_part,
            output_file => "$store_path/${prefix}_Zmoved_" . sprintf("%02d",$count) . ".data",
        );
        &heredoc(\%heredoc_hr);
        $count++; 
    }

}

#####here doc for data files##########
sub heredoc
{

my ($heredoc_hr) = @_;

#heredoc for the data file
my $heredoc = <<"END_MESSAGE";
$heredoc_hr->{first_part}
Atoms  # atomic

$heredoc_hr->{second_part}
END_MESSAGE

my $file = $heredoc_hr->{output_file};
open(FH, '>', $heredoc_hr->{output_file}) or die $!;
print FH $heredoc;
close(FH);
}



