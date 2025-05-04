import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyBBAX33_2v5UO_Ff2oP_M3MwdD2hSP8BRM",
    authDomain: "moontrip-455720-5ff09.firebaseapp.com",
    projectId: "moontrip-455720-5ff09",
    storageBucket: "moontrip-455720-5ff09.firebasestorage.app",
    messagingSenderId: "91979151084",
    appId: "1:91979151084:web:eb42d6f20527c2de69d7c9",
    measurementId: "G-TRCE2JWSCK"
};
const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

export { auth };
export default app;
