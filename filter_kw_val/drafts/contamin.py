def contamin_filter(mqfile, filter_file, output):
    # Read MaxQuant output file
    data = open(mqfile, "r")
    data = data.readlines()
    # Read filter file
    filterie = open(filter_file, "r")
    filterie = filterie.readlines()
    # Extract list of contaminants
    contamin = []
    for line in filterie[1:]:
        conta_prot = line.split()[0].split(";")
        for i in range(len(conta_prot)):
            contamin.append(conta_prot[i]) 
    #print(contamin)
    # MQ filter
    #output = open(mqfile.replace('.txt','_filted.txt'), "w")
    fileout = open(output, "w")
    i = 1
    for line in data[1:]:
        proID = line.split()[0].split(";")
        #print(proID)
        """for prot in proID:
            if prot not in contamin:
                output.write(line)"""
        if not any(ID in contamin for ID in proID):
            fileout.write(line)
            #print line
        #else:
            #print(i)
            #i += 1
    fileout.close()
    return fileout
if __name__ == "__main__":
    import sys
    mqfile, filter_file, output = sys.argv[1:]
    contamin_filter(mqfile, filter_file, output)
