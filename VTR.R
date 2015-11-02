merres<-function(Bb,n,x,t,X,T,p1x,p2x,p1y,p2y){
Bw<-(T-X*Bb)/(1-X)
bb<-(x*t-Bw*x*(1-x)+Bb*(1-x)^2)/(x^2+(1-x)^2)
bb[x==0]<-0
bw<-(t-x*bb)/(1-x)
bw[x==1]<-0
notinbox <- ifelse(bb>=0&bb<=1&bw>=0&bw<=1,FALSE,TRUE)
dp1 <- (Bb-p1x)^2+(Bw-p1y)^2
dp2 <- (Bb-p2x)^2+(Bw-p2y)^2
p12x<-ifelse(dp1<dp2,p1x,p2x)
bb[notinbox] <- p12x[notinbox]
bw<-(t-x*bb)/(1-x)
bw[x==1]<-0
list("Bb"=Bb,"Bw"=Bw,"bb"=bb,"bw"=bw)
}

merfun<-function(Bb,n,x,t1,X,T,p1x,p2x,p1y,p2y){
Bw<-(T-X*Bb)/(1-X)
bb<-(x*t1-Bw*x*(1-x)+Bb*(1-x)^2)/(x^2+(1-x)^2)
bb[x==0]<-0
bw<-(t1-x*bb)/(1-x)
bw[x==1]<-0
notinbox <- ifelse(bb>=0&bb<=1&bw>=0&bw<=1,FALSE,TRUE)
d <- (t1-x*Bb-(1-x)*Bw)^2/(x^2+(1-x)^2)
dp1 <- (Bb-p1x)^2+(Bw-p1y)^2
dp2 <- (Bb-p2x)^2+(Bw-p2y)^2
dp12<-ifelse(dp1<dp2,dp1,dp2)
p12x<-ifelse(dp1<dp2,p1x,p2x)
bb[notinbox] <- p12x[notinbox]
d[notinbox] <- dp12[notinbox]
bw<-(t1-x*bb)/(1-x)
bw[x==1]<-0
d <- d*n
sumd <- sum(d[x>0])
sumd
}

merill<-function(n,x,t){
wtx<-x*n
wtt<-t*n
T<-sum(wtt)/sum(n)
X<-sum(wtx)/sum(n)
P1X<-max(0,(X-(1-T))/X)
P2X<-min(1,T/X)
p1x<-ifelse(x>0,apply(cbind(0,(x-(1-t))/x),1,max),0)
p2x<-ifelse(x>0,apply(cbind(1,t/x),1,min),0)
p2y<-ifelse(x<1,apply(cbind(0,(t-x)/(1-x)),1,max),0)
p1y<-ifelse(x<1,apply(cbind(1,t/(1-x)),1,min),0)
opt<-optimize(merfun, c(P1X,P2X),n=n,x=x,t1=t,X=X,T=T,p1x=p1x,p2x=p2x,p1y=p1y,p2y=p2y)
res<-merres(opt$minimum,n=n,x=x,t=t,X=X,T=T,p1x=p1x,p2x=p2x,p1y=p1y,p2y=p2y)
}

bestpair<-function(n,X,T)
{
origX<-X
origT<-T
WMX<-mapply(FUN=weighted.mean,X,n)
if(min(WMX)<0.00001) {
#print(names(X)[which(WMX == min(WMX))])
X<-X[-which(WMX == min(WMX))]
WMX<-WMX[-which(WMX == min(WMX))]
}
WMT<-mapply(FUN=weighted.mean,T,n)
if(min(WMT)<0.00001) {
#print(names(T)[which(WMT == min(WMT))])
T<-T[-which(WMT == min(WMT))]
WMT<-WMT[-which(WMT == min(WMT))]
}
wcor<-diag(WMX)%*%cor(X,T)%*%diag(WMT)
newwcor<-wcor
#newwcor<-3*wcor-rowSums(wcor)
#newwcor<-t(t(newwcor)-colSums(wcor))
maxcor<-max(newwcor)
maxcol<-which.max(newwcor) %/% nrow(newwcor)
maxrow<-which.max(newwcor) %% nrow(newwcor)
if (maxrow>0) maxcol<-maxcol+1
if (maxrow==0) maxrow<-nrow(newwcor)
#cat(maxrow, maxcol, which.max(newwcor), "\n")
maxrow<-names(X)[maxrow]
maxcol<-names(T)[maxcol]
#cat(maxrow, maxcol, "\n")
maxrow<-grep(paste("^",maxrow,"$", sep=""), names(origX))
maxcol<-grep(paste("^",maxcol,"$", sep=""), names(origT))
#cat(maxrow, maxcol, "\n")
list("maxcol"=maxcol, "maxrow"=maxrow, "newwcor"=newwcor, "maxcor"=maxcor)
}

newdata<-function(newN,newX,newT,maxrow, maxcol, bb,totalbb){
tempbb<-newX[maxrow]*bb
nbb<-newN*tempbb
newN<-newN*(1-tempbb)
newX[maxrow]<-newX[maxrow]*(1-bb)
coefX<-1/rowSums(newX)
newX[is.finite(coefX),]<-newX[is.finite(coefX),]*coefX[is.finite(coefX)]
newT[maxcol]<-newT[maxcol]-tempbb
coefT<-1/rowSums(newT)
newT[is.finite(coefT),]<-newT[is.finite(coefT),]*coefT[is.finite(coefT)]
totalbb[,maxrow,maxcol]<-totalbb[,maxrow,maxcol]+nbb[,1]
list("newN"=newN,"newX"=newX,"newT"=newT,"totalbb"=totalbb,"nbb"=nbb)
}

multirate<-function(myN,myX,myT,stopat){
err<-1
if(isTRUE(all.equal(rowSums(myX),rep(1,nrow(myX)), 0.001))) err<-0
if(isTRUE(all.equal(rowSums(myT),rep(1,nrow(myT)), 0.001))) err<-0
totalbb<-array(0, dim=c(nrow(myN),length(myX),length(myT)))
newX<-myX; newT<-myT; newN<-myN
i<-0
while (sum(newN)/sum(myN)>stopat) {
i<-i+1
#cat (i, "\n")
best<-bestpair(newN,newX,newT)
res<-merill(newN,newX[best$maxrow],newT[best$maxcol])
newdt<-newdata(newN,newX,newT,best$maxrow,best$maxcol,res$bb,totalbb)
cat (i, names(newX[best$maxrow]), names(newT[best$maxcol]), sum(newdt$nbb)/sum(myX[best$maxrow]*myN), "\n")
newX<-newdt$newX; newT<-newdt$newT; newN<-newdt$newN ; totalbb<-newdt$totalbb
#cat (sum(myN), sum(newN), dim(totalbb), "\n")
}
absmyX<-myX*t(myN)
tempabsx<-unlist(absmyX,  use.names = FALSE)
absX<-matrix(tempabsx,ncol=length(myX)) 
finalbb<-newdt$totalbb
for (i in 1:length(myT)){
finalbb[,,i]<-newdt$totalbb[,,i]/absX
}
dimnames(finalbb)<-list(NULL,names(myX),names(myT))
dimnames(newdt$totalbb)<-list(NULL,names(myX),names(myT))
transitions<-array(0,dim=c(length(myX),length(myT)))
for (i in 1:length(myX)){
for (j in 1:length(myT)){
transitions[i,j]<-sum(newdt$totalbb[,i,j])/sum((myX[i]*myN))
}
}
dimnames(transitions)<-list(names(myX),names(myT))
list("Bb"=transitions, "bb"=finalbb)
}
