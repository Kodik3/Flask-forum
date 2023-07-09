import Request from './Request.js';

let login    = $("#login"),
    password = $("#password");

class Authorization{
    constructor(){this.APIAuthorization = "/api/v1/authorization";}

    authorize = async () => {
        try{
            const result = await Request.post(this.APIAuthorization,{
                "login" : login[0].value,
                "password" : password[0].value,
            });
            return result
        }
        catch (error) {console.log("Error:", error);}
    }
}

    
$("#log").click(async (e) => {
    e.preventDefault();
    let authorization = new Authorization();
    let result = await authorization.authorize();
    result = JSON.parse(result);
    console.log(result);
    
    if (result == 0){location.href="";}
    else if (result === 1) {
        $("#error").html("Wrong password");
      } 
      else if (result === 2) {
        $("#error").html("Your account was not found, register!");
      } 
    else{console.log("Error data");}
});