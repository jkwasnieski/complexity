"""
Takes snakemake object from file complexity.py
Requires completion of the following file types from pipeline:
 "{sample}/star/uniquely_mapping_reads.txt",
 "{sample}/star/sum_gene_mapping_reads.txt",
 "{sample}/star/unique_mapping_positions.txt",
Writes sample name, barcode, and complexity information to output file
"""
import pdb


def reshape_data(lookup, output):
	"""
	Takes a sample name and a list of files with one number each. Writes names and complexity metrics
	"""
	with open(output, 'w') as outfile:
		for condition, name in lookup.items():
			with open(name + "/star/sum_gene_mapping_reads.txt", 'r') as gene_reads_file:
				gene_reads = float(gene_reads_file.readline().rstrip())
			with open(name + "/star/unique_mapping_positions.txt", 'r') as positions_file:
				positions = float(positions_file.readline().rstrip())
			with open(name + "/star/uniquely_mapping_reads.txt", 'r') as total_file:
				total = total_file.readline().rstrip()
			outfile.write("\t".join( [condition, name, total, str(gene_reads/positions) + "\n" ]))	


def main():
	# pdb.set_trace()
	reshape_data(snakemake.config['lookup'], snakemake.output.file)




if __name__ == '__main__':
	main()
