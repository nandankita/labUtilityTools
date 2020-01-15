args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}
m <- sumMatrix <- read.table(paste("sumMatrixchr",args[1],sep=""), quote="\"", comment.char="")
m$V2[is.nan(m$V2)] <- 0
d<-(density(x=m$V2))
maxV<-d$x[which((d$y) == max(d$y))]
half<-maxV*0.6
v<-which(sumMatrix$V2<=half)
write.table(sumMatrix$V1[v], file = paste("unselectedIndexchr",args[1],sep=""),row.names=FALSE, col.names=FALSE, sep="\n", quote=FALSE)
#write.table(v, file = paste("unselectedIndexchr",args[1],sep=""),row.names=FALSE, col.names=FALSE, sep="\n", quote=FALSE)

sumMatrixchr23 <- read.delim("~/Downloads/sumMatrixchr23", header=FALSE)
m<-sumMatrixchr23

tmp<-chrD1.counts
tex="Clone D1"
plot(tmp$V1,tmp$V2,type ="l",xlab ="genomic bin",ylab ="genome coverage", main =tex)
plot(tmp$V1[1:31274],tmp$V2[1:31274],type ="l",xlab ="genomic bin",ylab ="genome coverage", main =tex)

for(i in seq(1:95)){
  abline(v=bin.pos$V2[i], col="red")
}

for(i in seq(1:95)){
  text(x=bin.pos$V2[i],y= max(tmp$V2)/2,bin.pos$V1[i],pos = 3, srt = 90, col="blue")
}



tmp1<-chrD3.counts
tmp2<-chrD7.counts
tex="log2(D1/D3)"
tmp<-log2(tmp1$V2/tmp2$V2)
#plot(tmp1$V1,tmp,type ="l",xlab ="genomic bin",ylab ="genome coverage", main =tex)
plot(tmp1$V1[1:31274],tmp[1:31274],type ="l",xlab ="genomic bin",ylab ="genome coverage", main =tex, ylim=c(-4,4))

for(i in seq(1:95)){
  abline(v=bin.pos$V2[i], col="red")
  text(x=bin.pos$V2[i],y=2,bin.pos$V1[i],pos = 3, srt = 90, col="blue")
}

a<-tmp[24256:24885]
a[is.nan(a)]<-0
sum(a)
