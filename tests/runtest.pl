#!/usr/bin/perl
if (-f "./hunspell") {
    $hunspell_cmd="./hunspell";
} else {
    $hunspell_cmd="hunspell" ;
}
$filename=$ARGV[0];
sub run_hunspell {
    my($word) = @_;
    my($dummy, $result,) = split(/\n/, `echo '$word' | $hunspell_cmd -d ../ko`);
    return $result;
}
open FILE, "<$filename";
while ($line = <FILE>) {
    next if ($line =~ /^#/);
    if ($line =~ /^([YN]) ([^\s]+)/) {
	$type = $1; $word = $2;
	$result = run_hunspell($word);
	$line = rindex($result, '\n');
	if (($type ne "Y" && ($result =~ /^[*+-]/)) ||
	    ($type ne "N" && ($result =~ /^[&]/))) {
	    print "$filename: $type $word: $result\n" ;
	    exit 1;
	}
    }
}
