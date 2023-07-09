// Request
import Request from './Request.js';

//------------|FORM|-------------|
let login = $("#login"),
    password = $("#password"),
    rpassword = $("#rpassword");
//-------------------------------|

class Registration {
  // Указываем куда будем отпровляеть запрос.
  constructor() {this.APIRegistration = "/api/v1/registration";}

  registrate = async () => {
    try {
      const result = await Request.post(this.APIRegistration,{
        "login": login[0].value,
        "password": password[0].value,
        "rpassword": rpassword[0].value,
      });
      return result;
    } 
    catch (error) {
    }
  }
}

$("#reg").click(async (e) => {
  e.preventDefault();
  let registration = new Registration();
  let result = await registration.registrate();
  result = JSON.parse(result);

  if (result === 0) {
    location.href = "";
  } 
  else if (result === 1) {
    $("#error").html("Repeat password is not correct!");
  } 
  else if (result === 2) {
    $("#error").html("Password cannot be less than 8 characters!");
  }
  else if (result === 3) {
    $("#error").html("User exists, please use a different username or log in with your account!");
  }
  else if (result === 4) {
    $("#error").html("Enter your name!");
  }
  else {
    console.log("Error data");
  }
});
