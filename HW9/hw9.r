#!/usr/bin/env Rscript

PlotGraph <- function(){
    plot(x, y)
    lines(d1$x1, d1$m1.fitted.values, col='red', lwd=5)
    lines(d2$x2, d2$m2.fitted.values, col='red', lwd=5)
}

Predict <- function(p){
    if(p <= 0){
        p = data.frame('x1'=p)
        return (predict(m1, p))
    }else{
        p = data.frame('x2'=p)
        return (predict(m2, p))
    }
}
PredictAll <- function(set){
    a = c()
    for (i in 1:length(set)){
        a[i] = Predict(set[i])
    }
    return (a)
}

data <- read.table(url("http://www.datagarage.io/api/5488687d9cbc60e12d300ba5"))
o <- seq(2, 4000, by=2)
d_c <- as.character(data[o, ])
p_m <- sapply(strsplit(d_c[], ""), function(d_c) which(d_c == ":"))
data <- data.frame(X=as.double(substr(d_c,p_m[2,]+1, 38)), Y=as.double(substr(d_c,p_m[1,]+1, 17)))
data1 <- data[data[, 'X'] <= 0,]
data2 <- data[data[, 'X'] > 0,]
x <- data$X
y <- data$Y
x1 <- data1$X
y1 <- data1$Y
x2 <- data2$X
y2 <- data2$Y

m1 <- lm(y1 ~ x1 + I(x1^2) + I(x1^3))
m2 <- lm(y2 ~ I(x2^0.5) + I(x2^0.333333) + I(x2^0.25))

d1 <- data.frame(x1, m1$fitted.values)
d1 <- d1[order(x1, m1$fitted.values),]

d2 <- data.frame(x2, m2$fitted.values)
d2 <- d2[order(x2, m1$fitted.values),]

py = PredictAll(data$X)
result = data.frame('X'=data$X, 'Y' = py)
write.table(result, file="result", row.names = FALSE)
