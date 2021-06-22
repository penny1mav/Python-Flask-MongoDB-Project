Ergasia_1_e17098_mavroeidi_panagiota
Για την εκπόνηση της εργασίας τα εργαλεία που θα χρειαστούν είναι τα εξής:
-editor : Visual Studio Code (κατα προτίμηση)

-Postman : μέσω του Postman μπορουμε ευκολα να αναπτυξουμε API

-Mongo DB Compass : Ειναι μια εφαρμογή για να βλέπουμε τι συμβαίνει στην βάση δεδομένων καθε στιγμή

Αρχικά θα χρειαστει να κάνουμε import το υπάρχον JSON αρχείο στο Mongo DB Compass ωστε να μπορουμε να εχουμε ανταπόκριση με την βάση δεδομένων

Ερωτημα 1 : Δημιουργία χρήστη
~Στην περίπτωση που: δεν εχουμε εκχωρίσει σωστά τα δεδομένα στο Body μέσω postman δεν εχουμε στείλει το σωστό request(εν προκειμενει POST) και δεν έχουμε εκχωρίσει όλα τα απαραίτητα στοιχεία θα υπάρξει error status 500 .

~Εφοσον εχουμε κανει λοιπον σωστά τα παραπάνω, η εφαρμογή δέχεται ως input το username και το password που εχουμε ορίσει στο body του Postman

~Πρωτού εκτελεστεί η εντολή που έχουμε ορίσει στο Postman, γίνεται έλεγχος αν το username υπαρχει ήδη στην βαση δεδομένων users.Αν το username υπάρχει τότε το postman μας στέλνει response ότι ο user υπάρχει ήδη

~Αν το username δεν υπαρχει στο db(database), εκχωρείται το username και password στο Mongo DB με ονομα users. Στην περίπτωση επιτυχίας μας γυρνάει το Postman ως response το παρακάτω
{}

Μπορούμε να το δούμε εύκολα χρησιμοποιώντας το Mongo db Compass

{}

Δίνοντας ως input μέσω postman ένα username και password θα γίνει έλεγχος εγκυρότητας μέσα στην βάση δεδομένων. Στην περίπτωση που ταυτοποιηθεί username και password το Postman γυρνάει ως Response το username που δώσαμε και ενα uuid , μια μεταβλητή που αλλάζει μετά από κάθε login session . Το uuid output θα μας χρειαστεί ως input στα επόμενα ερωτήματα.

{}

Στην περίπτωση που ή το username ή το password δεν είναι σωστό το Postman στέλνει ως response " Wrong username or password.". Οι users εχουν 2 κατηγοριες : user , admin . Και οι 2 χρηστες υπαρχουν απο πριν στην βαση ως json αρχεια. Admin υπαρχει μονο ενας fixed και δεν μπορει να προσθεθει αλλος με τις μεθοδους που εχουμε.



Ερώτημα 3 Αναζητηση Προιοντος:
Στο ερώτημα αυτό έχουμε διαφορετικό error status 500 . Στην περιπτωσή που δεν δώσουμε στο body του Postman το email , μας εμφανίζει information incomplete οπως βλέπουμε παρακάτω

Για να γίνει επιτυχής σύνδεση στο συστήμα θα πρέπει να κάνουμε αντιγραφή το uuid που μας δώθηκε στο login ως output και να το δηλώσουμε στα headers του postman όπως φαινεται παρακάτω
{}

Αυτό ισχύει και για τα επόμενα ερωτήματα . Συνεπώς , θεωρείται δεδομένο κάθε φορά που θα κάνουμε ενα νέο request θα πρέπει να φροντίζουμε να υπάρχει το uuid στα headers

Στην περίπτωση που δεν βάλουμε το σωστό uuid (πιθανόν λόγω αποσύνδεσης απο το σύστημα πρέπει να γίνει εκ νεου Login)

θα βγει ως Response "user is not authenticated". Η χρήση του uuid ισχύει ακριβώς η ίδια και στα επόμενα υποερωτήματα

Εφόσον λοιπον γίνει επιτυχής authentication η εφαρμογή μας δέχεται ως input το email που έχουμε δηλώσει στο postman. Στην σύνεχεια γίνεται μια αναζήτηση στο students db αν υπάρχει το δηλωθέν email.

Στην περιπτωσή που δεν υπάρχει έχουμε ως response "email does not exist "

Αν υπάρχει στην βάση δεδομένων γίνεται μια αναζήτηση μέσα σε μια επανάληψη. Εφόσον βρεθεί το email δημιουργείται ενα Dictionary με όνομα student που δέχεται και αποθηκεύει τις τιμές της βάσης δεδομένων Αφότου αποθηκεύσει τις τιμές αυτές το postman μας στέλνει ως response το Dictionary σε μορφη json (json.dumps).

{}


ΕΡΩΤΗΜΑ 4   Προσθηκη προιοντων στο καλαθι

Ο χρηστης εφοσον δωσει τα καταληλα στοιχεια στο body εμφανιζεται  το παρακατω καλαθι σε μορφη Dictionary

ΕΡΩΤΗΜΑ 5 Εμφανιση καλαθιου

ΕΡΩΤΗΜΑ 6 Διαγραφη προιοντος απο το καλαθι

ΕΡΩΤΗΜΑ 9 Διαγραφη του λογαριασμου .
ο χρηστης δινει στο body το email του και γινεται η διαγραφη του λογαριασμου του


ΕΡΩΤΗΜΑ 10
Για να μπορουμε να κανουμε τις επομενες λειτουργιες θα πρεπει να συνδεθουμε ως διαχειριστης , διοτι ο απλος user δεν εχει access σε αυτα τα endpoints
τα στοιχεια του admin υπαρχουν και στο Json αρχειο "users"

εφοσον γινεται η επιτυχης συνδεση του admin δινουμε στο body τα εξης στοιχεια και μας επιστρεφει το εξης αποτελεσμα
{}

ΕΡΩΤΗΜΑ 11
δινουμε στο body το id του προιοντος και γινεται αμεσα η διαγραφη του οπως βλεπουμε παρακατω

ΕΡΩΤΗΜΑ 12
δινουμε στο body τις τιμες και οσες θελουμε να αλαχθουν απλα οριζουμε την νεα τιμη τους οπως βλεπουμε παρακατω.
