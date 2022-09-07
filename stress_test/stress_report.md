# Stress test

Our tests will be conducted with users that hit the endpoints after a wait between 0.5 and 1 second.

Equipo con el que se realizan los tests:  
    - Procesador:     Intel(R) Core(TM) i5-6400 CPU @ 2.70GHz   2.70 GHz  
    - RAM instalada:  8,00 GB

---

## Test 1: 8 users

With 8 users using the endpoints there are no crushes or fails on any user.

![8 users](/stress_test/Test_1_-_8_users.JPG)


## Test 2: 9 users

With 9 users using the endpoints at the same time there are some timeouts:

<pre>
Type   Path       Request   Fails  

GET    /          1582      0  
POST   /predict   4548      16  
</pre>

![9 users](/stress_test/Test_2_-_9_users.JPG)

---

## Model scaled

<br>

Now we are going to conduct some scaling in the bottleneck of the service: the model
We are going to scale the 'model' container from 1 container to 4 of them.

<br>

## Test 3: 15 users

With 15 users using the endpoints there are no crushes or fails on any user when having 4 containers at the same time.

![15 users](/stress_test/Test_3_-_15_users_scaled=4.JPG)

## Test 4: 20 users

With 20 users using the endpoints at the same time there are some timeouts:

<pre>
Type   Path       Request   Fails  

GET    /          4485      0  
POST   /predict   13589     87  
</pre>

![20 users](/stress_test/Test_4_-_20_users_scaled=4.JPG)
