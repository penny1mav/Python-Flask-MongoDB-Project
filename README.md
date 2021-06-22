# Ergasia_2_e17098_mavroeidi_panagiota


# Για την  εκπόνηση της εργασίας τα εργαλεία που θα χρειαστούν είναι τα εξής:

-editor : Visual Studio Code (κατα προτίμηση)

-Postman : μέσω του Postman μπορουμε ευκολα να αναπτυξουμε API

-Mongo DB Compass : Ειναι μια εφαρμογή για να βλέπουμε τι συμβαίνει στην βάση δεδομένων καθε στιγμή

-VMWARE : για την υποστηριξη ι λογισμικou εικονικοποίησης

-ubuntu : για την υποστηριξη unix εντολων και την επιτυχη υλοποιηση image , docker compose


Αρχικά θα χρειαστει να κάνουμε import το υπάρχον JSON αρχείο στο Mongo DB Compass ωστε να μπορουμε να εχουμε ανταπόκριση με την βάση δεδομένων


# Ερωτημα 1 : Δημιουργία χρήστη

~Στην περίπτωση που:
 δεν εχουμε εκχωρίσει σωστά τα δεδομένα στο Body μέσω postman
 δεν εχουμε στείλει το σωστό request(εν προκειμενει POST) και
 δεν έχουμε εκχωρίσει όλα τα απαραίτητα στοιχεία
  θα υπάρξει error status 500 .

~Εφοσον εχουμε κανει λοιπον σωστά τα παραπάνω, η εφαρμογή  δέχεται ως input το username και το password που εχουμε ορίσει στο body του Postman 


~Πρωτού εκτελεστεί η εντολή που έχουμε ορίσει στο Postman, γίνεται έλεγχος αν το username υπαρχει ήδη στην βαση δεδομένων users.Αν το username υπάρχει τότε το postman μας στέλνει response ότι ο user υπάρχει ήδη

~Αν το email δεν υπαρχει στο db(database), εκχωρείται το username και password στο Mongo DB με ονομα users. Στην περίπτωση επιτυχίας μας γυρνάει το Postman ως response το παρακάτω


![createUser](https://user-images.githubusercontent.com/62929706/122966987-a745fd80-d392-11eb-9938-a042f401eb72.jpg)


 Μπορούμε να το δούμε εύκολα χρησιμοποιώντας το Mongo db Compass

![users](https://user-images.githubusercontent.com/62929706/122967111-ccd30700-d392-11eb-9c8f-52dd6f68cbf0.jpg)


# Ερώτημα 2: Login στο σύστημα

Δίνοντας ως input μέσω postman ένα email και password θα γίνει έλεγχος εγκυρότητας μέσα στην βάση δεδομένων.
Στην περίπτωση που ταυτοποιηθεί username και password το Postman γυρνάει ως Response το username που δώσαμε και ενα uuid , μια μεταβλητή που αλλάζει μετά από κάθε login session . Το uuid output θα μας χρειαστεί ως input  στα επόμενα ερωτήματα.


![login](https://user-images.githubusercontent.com/62929706/122967155-d6f50580-d392-11eb-84a7-63ccdbdfe833.jpg)

Στην περίπτωση που ή το username ή το password δεν είναι σωστό το Postman στέλνει ως response " Wrong username or password."

# Ερώτημα 3 Αναζητηση Προιοντος:

Στο ερώτημα αυτό έχουμε διαφορετικό error status 500 . Στην περιπτωσή που δεν δώσουμε στο body του Postman το id το ονομα και τη κατηγορια  , μας εμφανίζει information incomplete 

Για να γίνει επιτυχής σύνδεση στο συστήμα θα πρέπει να κάνουμε αντιγραφή το uuid που μας δώθηκε στο login ως output και να το δηλώσουμε στα headers του postman όπως φαινεται 

παρακάτω

![wrong_uuid](https://user-images.githubusercontent.com/62929706/119018728-118b0d00-b9a5-11eb-9686-b3145f7c34ba.jpg)

Αυτό ισχύει και για τα επόμενα ερωτήματα . Συνεπώς , θεωρείται δεδομένο κάθε φορά που θα κάνουμε ενα νέο request θα πρέπει να φροντίζουμε να υπάρχει το uuid στα headers

Στην περίπτωση που δεν βάλουμε το σωστό uuid (πιθανόν λόγω αποσύνδεσης απο το σύστημα πρέπει να γίνει εκ νεου Login)

θα βγει ως Response "user is not authenticated". Η χρήση του uuid ισχύει ακριβώς η ίδια και στα επόμενα υποερωτήματα

Εφόσον λοιπον γίνει επιτυχής authentication η εφαρμογή μας δέχεται ως input τα name category id που έχουμε δηλώσει στο postman. Στην σύνεχεια γίνεται μια αναζήτηση στο products db αν υπάρχει το εκαστοτε προιον ( ή προϊοντα) 



Στην περιπτωσή που δεν υπάρχει έχουμε ως response " does not exist "

Αν υπάρχει στην βάση δεδομένων γίνεται μια αναζήτηση μέσα σε μια επανάληψη. Εφόσον βρεθεί το προιον βασει id δημιουργείται ενα Dictionary με όνομα product που δέχεται και αποθηκεύει τις

τιμές της βάσης δεδομένων Αφότου αποθηκεύσει τις τιμές αυτές το postman μας στέλνει ως response το Dictionary σε μορφη json (json.dumps). 




![getProductById](https://user-images.githubusercontent.com/62929706/122967270-f9871e80-d392-11eb-8b59-530c08e7c55e.jpg)







{}


Αν βρεθει προιον βασει κατηγοριας η ονοματος δημιουργειται μια λιστα με dictionaries . Αυτο συμβαινει διοτι το Id του προιοντος ειναι μοναδικο ενω το ονομα ή η κατηγορια ειναι ενα η περισσοτερα


![getProductByCategory](https://user-images.githubusercontent.com/62929706/122967239-ef652000-d392-11eb-9530-c030ae75babd.jpg)


![getProductByName](https://user-images.githubusercontent.com/62929706/122967304-00159600-d393-11eb-9629-940dd5ece094.jpg)



#ΕΡΩΤΗΜΑ 4   Προσθηκη προιοντων στο καλαθι

Ο χρηστης εφοσον δωσει τα καταληλα στοιχεια στο body εμφανιζεται  το παρακατω καλαθι σε μορφη Dictionary


![shoppingCart](https://user-images.githubusercontent.com/62929706/122967352-0c99ee80-d393-11eb-8174-d2c4641b6527.jpg)



# ΕΡΩΤΗΜΑ 5 Εμφανιση καλαθιου


![getShoppingCart](https://user-images.githubusercontent.com/62929706/122967390-14f22980-d393-11eb-9749-e81359b970ce.jpg)


# ΕΡΩΤΗΜΑ 6 Διαγραφη προιοντος απο το καλαθι


![deleteCart](https://user-images.githubusercontent.com/62929706/122967425-1f142800-d393-11eb-9042-f34dc500a8b3.jpg)



# ΕΡΩΤΗΜΑ 9 Διαγραφη του λογαριασμου .





ο χρηστης δινει στο body το email του και γινεται η διαγραφη του λογαριασμου του


![deleteUser](https://user-images.githubusercontent.com/62929706/122968556-5505dc00-d394-11eb-9e9b-49dc9b7f86b3.jpg)



# ΕΡΩΤΗΜΑ 10
Για να μπορουμε να κανουμε τις επομενες λειτουργιες θα πρεπει να συνδεθουμε ως διαχειριστης , διοτι ο απλος user δεν εχει access σε αυτα τα endpoints
τα στοιχεια του admin υπαρχουν και στο Json αρχειο "users"


![adminlogin](https://user-images.githubusercontent.com/62929706/122967579-4539c800-d393-11eb-9f8e-cbf1c298565e.jpg)




εφοσον γινεται η επιτυχης συνδεση του admin δινουμε στο body τα εξης στοιχεια και μας επιστρεφει το εξης αποτελεσμα




![addProduct](https://user-images.githubusercontent.com/62929706/122967603-4d920300-d393-11eb-92f9-7970ff29b39a.jpg)


βλεπουμε στο Mongo db compass πως το product ham δημιουργηθηκε


![ham](https://user-images.githubusercontent.com/62929706/122967650-5be01f00-d393-11eb-919b-1b5285ffac11.jpg)



# ΕΡΩΤΗΜΑ 11
δινουμε στο body το id του προιοντος και γινεται αμεσα η διαγραφη του οπως βλεπουμε παρακατω


![deleteham](https://user-images.githubusercontent.com/62929706/122967622-5551a780-d393-11eb-9674-40c621e3ab53.jpg)




# ΕΡΩΤΗΜΑ 12
δινουμε στο body τις τιμες και οσες θελουμε να αλαχθουν απλα οριζουμε την νεα τιμη τους οπως βλεπουμε παρακατω.

![milkupdated](https://user-images.githubusercontent.com/62929706/122967783-7f0ace80-d393-11eb-9c6c-5791fcfb08cf.jpg)


![update](https://user-images.githubusercontent.com/62929706/122967797-8500af80-d393-11eb-8a62-e81a6ceb71c3.jpg)

Αυτο που μας μενει ειναι να κανουμε docker compose την εργασια.

ανοιγουμε το vmware το συνδεουμε με ubuntu και ανοιγουμε το terminal

στη συνεχεια κανουμε copy paste τους κωδικες του app.py DockerFile και docker-compose.yml σε 3 διαφορετικα scriptakia

στο τελος κανουμε docker build το app.py για να φτιαξουμε το Image της εργασιας και τελος κανουμε docker-compose up 

