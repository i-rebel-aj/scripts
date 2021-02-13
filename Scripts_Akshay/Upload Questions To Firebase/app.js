const admin = require("firebase-admin");
const firestoreService = require('firestore-export-import');
const serviceAccount = require("./service_config.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db= admin.firestore();
// JSON To Firestore
const jsonToFirestore = async () => {
  try {
    console.log('Initialzing Firebase');
    await firestoreService.initializeApp(serviceAccount,"https://quesparser.firebaseio.com/");
    console.log('Firebase Initialized');

    await firestoreService.restore("./Questions.json");
    console.log('Upload Success');
  }
  catch (error) {
    console.log(error);
  }
};

//Comment this line if you don't want to save question to firebase
jsonToFirestore();