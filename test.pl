#!/usr/local/bin/perl 
use strict;
no warnings 'experimental::smartmatch';

sub add_vertex {
	my $graphRef = shift;
	my $v = shift;
	if (exists ($graphRef->{$v})) {
		print "Vertex $v already exists.\n";
	} else {
		$graphRef->{$v} = ();
	}
}

sub add_edge {
	my ($graphRef, $v1, $v2, $w) = @_;
	if (not exists ($graphRef->{$v1})) {
		print "Vertex $v1 does not exist.\n";
		exit 0;
	} elsif (not exists ($graphRef->{$v2})) {
		print "Vertex $v2 does not exist.\n";
		exit 0;
	} else {
		my @temp = ($v2, $w);
		push @{$graphRef->{$v1}}, [@temp];
	}
}

sub print_graph {
	#my $graphRef = shift;
	#my $graph = shift;#%{$graphRef};
	my %g = @_;
	#print "graph\n";
	while (my ($v, $e) = each (%g)) {
		if (defined $e) {
			my @edges = @{$e};
			foreach (@edges) {
				print "$v -> ${$_}[0], edge weight: ${$_}[1]\n";
			}
		}
	}
}

sub print_graph_to_gephi {
	#my ($file, %graph, $node, $edge) = @_;
	my $file = shift;
	my $graphRef = shift;
	my $node = shift;
	my $edge = shift;
	open(OUT2, ">$file.gexf");
	print OUT2 "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
	print OUT2 "<gexf xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" ",
	"version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n";
	print OUT2 "<meta lastmodifieddate=\"2020-05-08+6:30\">\n";
	print OUT2 "<creator>Gephi 0.7</creator>\n";
	print OUT2 "</meta>\n";
	print OUT2 "<graph defaultedgetype=\"directed\" idtype=\"string\" ",
	"type=\"static\">\n";
	print OUT2 "<nodes count=\"$node\">\n";
	foreach my $n (keys %{$graphRef}) {
		print OUT2 "<node id=\"$n\" label=\"$n\"/>\n";
	}
	print OUT2 "</nodes>\n";
	print OUT2 "<edges count=\"$edge\">\n";
	my $counter = 0;
	while (my ($n, $links) = each (%{$graphRef})) {
		if (defined $links) {
			#print "links = $links\n";
			my @link = @{$links};
			#print "@link\n";
			foreach my $e (@link) {
				my $target = ${$e}[0];
				my $w = ${$e}[1];
				print OUT2 "<edge id=\"$counter\" source=\"$n\" target=\"$target\" weight=\"$w\"/>\n";
				$counter += 1;
			}
		}
	}
	print OUT2 "</edges>\n";
	print OUT2 "</graph>\n";
	print OUT2 "</gexf>\n";
	close(OUT2);
}



my %graph;
#add_vertex(\%graph, "1");
#print %graph, "\n";
#my $size = keys %graph;

#add_vertex(\%graph, "n2");
#print %graph, "\n";
#my $size = keys %graph;
#my @t = keys %graph;
#print "size = $size\nitems=@t\n";

#add_edge(\%graph, "1", "n2", 2);
#print %graph, "\n";
#my $size = keys %graph;
#my @t = keys %graph;
#print "size = $size\nitems=@t\n";

#print_graph(%graph);
my %des;
open(IN, "test.ll");
#open(IN, "test.ll");
#open(IN, "temp.ll");
print "Starting...\n";
my $node = 0;
my $edge = 0;

while(<IN>) {
	chomp;
	$_ =~ tr/,<>\[\]\(\).//d;
	my @opcodes = split;
	my $flag = 0;
	my $desRg;
	my @srcRg;
	$node += 1;
	add_vertex(\%graph, $node);
	if ($opcodes[0] =~ /%/) {
		# it is an instruction with '='
		# destination register appears on the left
		# side of '='
		for my $op (@opcodes) {
			if ($op =~ /%/ and $flag == 0) {
			# usually destination register
			# since flag = 0
				$desRg = $op;
			} elsif ($op =~ /%/ and $flag == 1) {
			# usually source registers
			# since flag = 1
				push @srcRg, $op;
			} elsif ($op =~ /=/) {
				$flag = 1;
			} 
		}
		# check dependencies, construct graphs
		OUTER: foreach my $s (@srcRg) {
			print "source: $s\n";
			INNER: foreach my $i (keys %des) {
				if ($s eq $i) {
					add_edge(\%graph, $des{$s}, $node, 1);
					$edge += 1;
					last INNER;
				}
			}
		}
		$des{$desRg} = $node;
	} elsif ($opcodes[0] =~ /store/) {
		# store instruction
		# first register is source;
		# second is dest;
		# But occaionally there's only dest reg.
		my @Rg;
		for my $op (@opcodes) {
			if ($op =~ /%/) {
				push @Rg, $op;
			}
		}
		my $size = @Rg;
		if ($size == 1) {
			# one des and one source
			add_edge(\%graph, $des{$Rg[0]}, $node, 1);
			$edge += 1;			
			$des{$Rg[0]} = $node;
		} elsif ($size == 2) {
			# two sources one dest
			my $source1 = $Rg[0];
			my $source2 = $Rg[1];
			my $dest = $Rg[1];
			add_edge(\%graph, $des{$source1}, $node, 1);
			add_edge(\%graph, $des{$source2}, $node, 1);
			$edge += 2;			
			$des{$dest} = $node;
		}
	} elsif ($opcodes[0] =~ /call/) {
		# call instruction
		for my $op (@opcodes) {
			if ($op =~ /%/) {	
				add_edge(\%graph, $des{$op}, $node, 1);
				$edge += 1;		
			}
		}
		add_vertex(\%graph, $node+1);
		add_edge(\%graph, $node, $node+1, 1);

	} else {
		print "Sorry, this instruction @opcodes is not recognized.\n";
		print "The program is aborted.\n";
		print "Contact Yao for further mentenancce.\n";
		exit 0;
	}
}

close(IN);

undef %des;

print_graph(%graph);
print("#nodes = $node\n");
print("#edges = $edge\n");
print_graph_to_gephi("test", \%graph, $node, $edge);