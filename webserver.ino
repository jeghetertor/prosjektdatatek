#include <WiFi.h>
const char* ssid = ""; //internett navn
const char* password = ""; //passord
WiFiServer server(80); //setter server til port 80
String header;//variabelen gjør at en lagrer oversktiften til HTTP forespørselen
//linjen under gjør at Arduino klarer å lese HTML koden under 
char webpage[] PROGMEM = R"=====(
<!DOCTYPE html>
<html lang="en">
<meta charset="utf-8"><!-- for å få med bokstavene æøå-->
<body>
<style>/*CSS implementering*/

    body {
        width: 650px;
        margin: 0 auto;
        padding: 50px;
        background-color: darkcyan;
        color: white;
    }

    div.group {
        margin: 20px 0;
    }

    div.group.inlined {/*gjør at utsjekk dato står ved siden av innsjekk dato*/
        width: 49%;
        display: inline-block;
        float: left;

    }

    label {
        display: block;
        padding-bottom: 10px;
        font-size: 1.25em;
    }

    input, select, textarea {
        border-radius: 2px;
        border: 2px solid #777;
        box-sizing: border-box;
        font-size: 1.25em;
        width: 100%;
        padding: 10px;
    }

    div.group.inlined input {
        width: 95%;
        display: inline-block;
    }

    textarea {
        height: 250px;
    }

    button {
        height: 50px;
        background: lightgreen;
        border: none;
        color: white;
        font-size: 1.25em;
        border-radius: 4px;
        cursor: pointer;

    }

    button:hover {
        border: 2px solid darkcyan;
    }

</style>

<script>//javascript 
    var today = new Date();//henter dato og klokketid
    var timeNow = today.getHours() + ":" + today.getMinutes();//lagrer variabel for klokka nå, i format time:minutter
    function myClick() {//hva som skal skje når knappen trykkes
     const database =  firebase.database();//variabel som refererer til databasen
      var nameV   = document.getElementById("name").value;//henter verdi fra navn imput med Id name
      var nameVisited  = document.getElementById("nameHousehold").value;//henter navn på hvem som besøkens med Id nameHousehold
      var tlfV = document.getElementById("phone").value;
      var emailV = document.getElementById("email").value;
      var messageV = document.getElementById("message").value;
      var checkout = document.getElementById("checkout").value;
      var dateIn = document.getElementById("checkindate").value;
      var dateOut = document.getElementById("checkoutdate").value;
      var data = "Du har blitt registrert! " +nameV + ", " + emailV+", "+tlfV+".";//meldig du får etter å ha registrert deg
      const rootRef = firebase.database().ref("Gjester");//refererer til root plassering i databasen

      if(nameV === ""){//burde legges til slik betingelse for flere felt, slik at det meste av input felt blir fylt ut
      alert("Du har ikke fylt ut navnet ditt!");
      }else{

        rootRef.child(nameVisited).push({//data sendes til den genererte plasseringen
            navn: nameV,//legger inn navn i databsen
            telefon:tlfV,
            epost: emailV,
            melding: messageV,
            ankom_kl: timeNow,
            dro_kl: checkout,
            ankom_dato: dateIn,
            navn_beboer:nameVisited
            
        });
        document.write("Du har blitt registrert! " +nameV + ", " + emailV+", "+tlfV+".");//vil tømme dokumentet/nettsiden, slik at teksten kun dukker opp på nettside
    }
}

</script>

    <form>
        <h2 style="text-align:center;">Registrer ditt besøk her:</h2><!--overskrift type 2-->

        <div class="group">
            <label for="name">Ditt navn</label>
            <input type="text" id="name" name="visitor_name" placeholder="" pattern=[A-Z\sa-z]{3,20} required><!--input felt navn-->
        </div>
        <div class="group">
        <label for="beboere">Hvem besøker du?</label>
        <select id="nameHousehold" name="Beboere"><!--lager en drop down meny-->
           <option value="Maja">Maja</option>
            <option value="Hanne">Hanne</option>
            <option value="Hanna">Hanna</option>
            <option value="Tor">Tor</option>
            <option value="Nina">Nina</option>
        </select>
        </div>

        <div class="group">
            <label for="email">E-post</label>
            <input type="email" id="email" name="visitor_email" placeholder="" required>
        </div>

        <div class="group">
            <label for="phone">Telefon nr.</label>
            <input type="tel" id="phone" min = 8 name="visitor_phone" placeholder="" pattern=(\d{3})-?\s?(\d{3})-?\s?(\d{4}) required>
        </div>

         <div class = "group">
             <label for="checkout">Utsjekk tid</label>
             <input type="time" id="checkout" name="checkout" required>
         </div>

        <div class="group inlined">
            <label for="checkin">Innsjekk dato</label>
            <input type="date" id="checkindate" name="checkindate" required>
        </div>

        <div class="group inlined">
            <label for="checkout">Utsjekk dato</label>
            <input type="date" id="checkoutdate" name="checkoutdate" required>
        </div>

        <div>
            <textarea id="message" name="visitor_message" placeholder="Anything else?" required></textarea><!--lager tekstfelt-->
        </div>

        <div style="text-align:center;">
            <button onclick="myClick()" id= "but" type="button">Registerer ditt besøk!</button><!--knapp som utfører myClick() funksjonen når trykket-->
        </div>

    
<script src="https://www.gstatic.com/firebasejs/8.4.1/firebase-app.js"></script><!--firebase kjerne klienten-->
<script src="https://www.gstatic.com/firebasejs/8.4.1/firebase-database.js"></script><!--firebase realtime database-->


<script>//veldig viktig at dette står i slutten av HTML koden!
    // Your web app's Firebase configuration
    var firebaseConfig = {
        apiKey: "AIzaSyDFL7uysmbIJlMmmfhGWlZkDoDU0Vxy8RE",
        authDomain: "prosjekt-vaar-2021.firebaseapp.com",
        databaseURL: "https://prosjekt-vaar-2021-default-rtdb.firebaseio.com",
        projectId: "prosjekt-vaar-2021",
        storageBucket: "prosjekt-vaar-2021.appspot.com",
        messagingSenderId: "542991120548",
        appId: "1:542991120548:web:526306da410175eeae8e31"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
</script>

    </form>
  </body>

</html>

)=====";


void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);//kobler il internett
  Serial.print("Connecting to ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());// this will display the Ip address of the Pi which should be entered into your browser
  server.begin();

}

void loop() {
  WiFiClient client = server.available();   // leter etter inkommende klienter
  if (client) {                             // hvis en nye klient kobles til,
    String currentLine = "";                // string som holder inkommende data fra klienten
    while (client.connected()) {            // loop mens klienten er koblet til
      if (client.available()) {             // hvis det er bytes en kan lese fra klienten,
        char c = client.read();             // leser en byte
        Serial.write(c);                    // skriver ut til seriell overvåker
        header += c;
        if (c == '\n') {                    // hvis byten er en ny linje char
          // hvis denne linjen er blank, får du to ny linje char etter hverandre
          
          if (currentLine.length() == 0) {
            // HTTP overskrifter starter alltid med koden (e.g. HTTP/1.1 200 OK)
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            client.println(webpage);
            client.println();
           
            break; // går ut av while loop
          } else { 
            currentLine = "";
          }
        } else if (c != '\r') {  
          currentLine += c;      
         }
    
      }
    }
  }
}
