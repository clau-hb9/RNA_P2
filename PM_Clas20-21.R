library(RSNNS)

# Funciones

graficaError <- function(iterativeErrors){
  plot(1:nrow(iterativeErrors),iterativeErrors[,1], type="l", main="Evolucion del error",
       ylab="MSE (3 salidas)",xlab="Ciclos",
       ylim=c(min(iterativeErrors),max(iterativeErrors)))
  lines(1:nrow(iterativeErrors),iterativeErrors[,2], col="red")
}


accuracy <- function (cm) sum(diag(cm))/sum(cm)


set.seed(1)

#CARGA DE LOS DATOS
# cambiar a fold 2 y 3

fold <- 4


# usar read.table si los campos estan separados por espacios o tabuladores. 
# Si estan separados por ; o , usar read.csv

#trainSet <- read.table(paste("Train",fold,".txt",sep=""),header = T)
#testSet  <- read.table(paste("Test", fold,".txt",sep=""),header = T)

trainSet <- read.csv(paste("DatosProcesados/Modelo_",fold,"/datosNubes_entrenamiento.txt",sep=""),dec=".",sep=",",header = T)
testSet  <- read.csv(paste("DatosProcesados/Modelo_",fold,"/datosNubes_test.txt",sep=""),dec=".",sep=",",header = T)


#SELECCION DE LA SALIDA. Num de columna del target. 
nTarget <- ncol(trainSet)    

#SEPARAR ENTRADA DE LA SALIDA
trainInput <- trainSet[,-nTarget]
testInput <-  testSet[,-nTarget]


#TRANSFORMAR LA SALIDA DISCRETA A NUMERICA (Matriz con columnas, una por etiqueta, hay un 1 por cada fila en la columna que pertenece a la clase)
trainTarget <- decodeClassLabels(trainSet[,nTarget])
testTarget <-  decodeClassLabels(testSet[,nTarget])

# transformar las entradas de dataframe en matrix para mlp: 
trainInput <- as.matrix(trainInput)
testInput  <- as.matrix(testInput )


#SELECCION DE LOS HIPERPARAMETROS DE LA RED
topologia        <- c(10)
razonAprendizaje <- 0.01
ciclosMaximos    <- 1200

## generar un nombre de fichero que incluya los hiperparametros
fileID <- paste("fold_",fold,"_topol",paste(topologia,collapse="-"),"_ra",
                razonAprendizaje,"_iter",ciclosMaximos,sep="")

set.seed(1)
#EJECUCION DEL APRENDIZAJE Y GENERACION DEL MODELO
model <- mlp(x= trainInput,
             y= trainTarget,
             inputsTest= testInput,
             targetsTest= testTarget,
             size= topologia,
             maxit=ciclosMaximos,
             learnFuncParams=c(razonAprendizaje),
             shufflePatterns = F
)

#GRAFICO DE LA EVOLUCION DEL ERROR
#
#plotIterativeError(model)

#TABLA CON LOS ERRORES POR CICLO de train y test correspondientes a las 4 salidas
iterativeErrors <- data.frame(MSETrain= (model$IterativeFitError/nrow(trainSet)),
                              MSETest= (model$IterativeTestError/nrow(testSet)))

graficaError(iterativeErrors)


#GENERAR LAS PREDICCIONES en bruto (valores reales)
trainPred <- predict(model,trainInput)
testPred  <- predict(model,testInput)

#poner nombres de columnas "cieloDespejado" "multinube" "nube" 
colnames(testPred)<-colnames(testTarget)
colnames(trainPred)<-colnames(testTarget)

# transforma las tres columnas reales en la clase 1,2,3 segun el maximo de los tres valores. 

trainPredClass<-as.factor(apply(trainPred,1,which.max))  
testPredClass<-as.factor(apply(testPred,1,which.max)) 

#transforma las etiquetas "1", "2", "3" en "cieloDespejado" "multinube" "nube"
levels(testPredClass)<-c("cieloDespejado", "multinube","nube")
levels(trainPredClass)<-c("cieloDespejado", "multinube","nube")


#CALCULO DE LAS MATRICES DE CONFUSION
trainCm <- confusionMatrix(trainTarget,trainPred)
testCm  <- confusionMatrix(testTarget, testPred)

trainCm
testCm

#VECTOR DE PRECISIONES
accuracies <- c(TrainAccuracy= accuracy(trainCm), TestAccuracy=  accuracy(testCm))

accuracies


# calcular errores finales MSE
MSEtrain <-sum((trainTarget - trainPred)^2)/nrow(trainSet)
MSEtest <-sum((testTarget - testPred)^2)/nrow(testSet)

MSEtrain
MSEtest

#GUARDANDO RESULTADOS
#MODELO
saveRDS(model,            paste("nnet_",fileID,".rds",sep=""))

#tasa de aciertos (accuracy)
write.csv(accuracies,     paste("finalAccuracies_",fileID,".csv",sep=""))

#Evolucion de los errores MSE
write.csv(iterativeErrors,paste("iterativeErrors_",fileID,".csv",sep=""))

#salidas esperadas de test con la clase (Target) (ultima columna del fichero de test)
write.csv( testSet[,nTarget] ,      paste("TestTarget_",fileID,".csv",sep=""), row.names = TRUE)


#salidas esperadas de test codificadas en tres columnas (Target)
write.csv(testTarget ,      paste("TestTargetCod_",fileID,".csv",sep=""), row.names = TRUE)


#salidas de test en bruto (nums reales)
write.csv(testPred ,      paste("TestRawOutputs_",fileID,".csv",sep=""), row.names = TRUE)

#salidas de test con la clase
write.csv(testPredClass,  paste("TestClassOutputs_",fileID,".csv",sep=""),row.names = TRUE)

# matrices de confusion
write.csv(trainCm,        paste("trainCm_",fileID,".csv",sep=""))
write.csv(testCm,         paste("testCm_",fileID,".csv",sep=""))