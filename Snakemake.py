rule all:
	"report.txt"


rule bam_to_intersect_bed:
	"""Intersect aligned reads with gene exons. Return bed file"""
	output:
		"{sample}/star/intersect_bed.txt"
	input:
		bam = "{sample}/star/Aligned.sortedByCoord.out.bam",
		bed = config["refflat"].replace('.txt', '.bed')
	shell:
		"intersectBed -abam {input.bam} -b {input.bed} -bed -wb -s > {output}"


rule sum_gene_mapping_reads:
	"""Report the number of gene mapping reads"""
	output:
		temp("{sample}/star/sum_gene_mapping_reads.txt")
		# "{sample}/star/sum_gene_mapping_reads.txt"
	input:
		by_gene = "{sample}/star/genes_compiled.txt"
	shell:
		"cat {input.by_gene} | awk '{{sum += $1}}; END{{print sum}}' >> {output}"



rule uniquely_mapping_reads:
	"""Report the number of uniquely mapping reads"""
	output:
		temp("{sample}/star/uniquely_mapping_reads.txt")
		# "{sample}/star/uniquely_mapping_reads.txt"
	input:
		star_log = "{sample}/star/Log.final.out"
	shell:
		"grep 'Uniquely mapped reads number' {input.star_log} | awk '{{print $6}}' >> {output}"


rule unique_mapping_positions:
	"""Report the number of unique mapping positions """
	output:
		temp("{sample}/star/unique_mapping_positions.txt")
		# "{sample}/star/unique_mapping_positions.txt"
	input:
		bed = "{sample}/star/intersect_bed.txt"
	params:
		fields = "13,16,18,7,8"
	shell:
		"cut -f {params.fields} {input.bed} | sort | uniq | wc -l >> {output}"


rule report:
	"""Report the complexity information for sequencing run"""
	output:
		file = "report.txt"
	input:
		unique_mappers = expand("{sample}/star/uniquely_mapping_reads.txt", sample=config["lookup"].values()),
		gene_mappers = expand("{sample}/star/sum_gene_mapping_reads.txt",sample=config["lookup"].values()),
		unique_positions = expand("{sample}/star/unique_mapping_positions.txt",sample=config["lookup"].values())
	script:
		"calculate_complexity.py"




# rule picard_estimate_complexity:
# 	""" Use Picard tools to estimate complexity of the sample"""
# 	output:
# 		file = "{sample}/star/picard/est_lib_complex_metrics.txt"
# 	input:
# 		bam = "{sample}/star/Aligned.sortedByCoord.out.bam"
# 	shell:
# 		"/usr/local/jdk1.8/bin/java -jar /usr/local/share/picard-tools/picard.jar EstimateLibraryComplexity I={input.bam} O={output.file}"

