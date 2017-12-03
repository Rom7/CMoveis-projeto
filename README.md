##### 2/12/2017 : A versão atual no GitHub é uma implementação de outra abordagem com Linear Regression + Artificial Neural Network. A versão final apresentada está descrita abaixo.

# Comunicaçoes Móveis : Projeto

Geo-tracker project based on machine learning and radio propagation model. A mobile RSSI measure is used to estimate the user's position.
#### 1. Database :
   - *erbs.csv* : RBS informations (name, position, equivalent isotropically radiated power...)
   - *medicoes.csv* : received signal strength indication (RSSI) measurements for training (training data)
   - *testLoc.csv* : test data (input : RSSI from each RBS)
   - *fichier-test.csv* : computed data (output : WGS84 position)
#### 2. Aproach / Abordagem (Python / Numpy / Pandas / Sklearn / Keras) :
   - 1: Model fitting (remove duplications, similar entries...)
   - 2: Train a weighted k-nearest neighbors (w-KNN) algorithm with the fitted model
   - 3: w-KNN computes a 6-dimensional vector for each points (input) : each dimension represents a distance to an RBS
   - 4: Particle Swarm Optimization (PSO) algorithm is used to solve the non-linear optimization problem : compute user's position by minimizing the distance to each RBS.
   - 5: RMSE global and RMSE for input are displayed (10X-validation) : side-effects can be observed depending on training data and/or input repartition (step 1 minimize those side-effects). 
#### 3. Data visualization (JavaScript / D3.js / Leaflet.js) :
   - 1: Python code writes the coordinates in *fichier-test.csv*
   - 2: *datavis-format.js* loads all data and computes a graphic rendering in *renderer.html*
   - 3: User can chose 2 ways to visualize : 
      - "Visualização global" : all the points (the real ones in red, computed in yellow)
      - "Visualização passo-a-passo" : all computed points are displayed (yellow) and can be clicked. A click on a point will display on the map (red) the real associated point.
 

