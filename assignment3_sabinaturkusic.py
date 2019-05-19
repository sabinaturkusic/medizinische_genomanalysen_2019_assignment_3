#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Sabina Turkusic'

## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
## 4) View the VCF in a browser

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"  # TODO

    def annotate_vcf_file(self):

        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        annotation_dataset = json.loads(annotation_result)

        return annotation_dataset

    
    def get_list_of_genes(self, annotation_dataset):
        genenames = []
        for line in annotation_dataset:
            if "cadd" in line:
                if "genename" in line["cadd"]["gene"]:
                    genenames.append(line["cadd"]["gene"]["genename"])
        print("List of genenames: ", genenames)

    def get_num_variants_modifier(self, annotation_dataset):
        counter = 0
        for line in annotation_dataset:
            if "snpeff" in line:
                key, value = "putative_impact", "MODIFIER"
                if key in line["snpeff"]["ann"] and value == line["snpeff"]["ann"]["putative_impact"]:
                    counter += 1
        print("Number of variants with putative impact 'MODIFIER': ", counter)

    def get_num_variants_with_mutationtaster_annotation(self, annotation_dataset):
        counter = 0
        for line in annotation_dataset:
            if "dbnsfp" in line:
                if "mutationtaster" in line["dbnsfp"]:
                    counter += 1
        print("Number of variants with mutationtaster annotation: ", counter)
        
    
    def get_num_variants_non_synonymous(self, annotation_dataset):
        counter = 0
        for line in annotation_dataset:
            if "cadd" in line:
                key, value = "consequence", "NON_SYNONYMOUS"
                if key in line ["cadd"] and value == line["cadd"]["consequence"]:
                    counter += 1
        print("Number of 'non-synonymous’ variants: ", counter)
        
    
    def view_vcf_in_browser(self):
        ## Document the final URL here
        print("The vcf file was compressed and indexed and the results were visualized with the vcf.iobio website (URL of results: https://vcf.iobio.io/?species=Human&build=GRCh38).")
        print("The reference selection shows that chr16 is available for analysis.")
        print("The distribution of variants is mostly very equal. BUT: there are higher peaks at 12M and 47 M and in the area around 32-37M.")
        print("The base changes plot shows that A is more likely to mutate to G and vice versa and C is likely to mutate to T and vice versa. Which is not unusual.")
        print("The most variant types found are SNPs, Insertions and Deletions are only found to a small extent.")
        print("The variant quality score can not be read properly. Therefore, I can’t interpret this plot.")
    
    def print_summary(self):
        dataset = self.annotate_vcf_file()
        self.get_list_of_genes(dataset)
        self.get_num_variants_modifier(dataset)
        self.get_num_variants_with_mutationtaster_annotation(dataset)
        self.get_num_variants_non_synonymous(dataset)
        self.view_vcf_in_browser()


def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



