args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}
neworder <- read.table("selectedOrder", quote="\"", comment.char="")
clusterRearranged<-read.table(gzfile(args[1]), header=T, row.names=1)
neworderDim<-dim(neworder)[1]
newMatrix<-matrix(NA,nrow=neworderDim,ncol=neworderDim)
colnames(newMatrix)<-neworder[,1]
rownames(newMatrix)<-neworder[,1]
for(i in neworder[,1]){
        for(j in neworder[,1]){
                newMatrix[i,j]<-clusterRearranged[i,j]
        }
}
print(sum(clusterRearranged))
print(sum(newMatrix))
gz1 <- gzfile( paste(args[1],"removedbins.incorrectHeader.matrix.gz",sep="."), "w")
write.table(newMatrix, file=gz1, sep = "\t", quote = FALSE, row.names = TRUE, col.names = TRUE)
close(gz1)