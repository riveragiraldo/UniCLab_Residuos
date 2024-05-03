document.addEventListener("DOMContentLoaded", function () {
    const password1Input = document.getElementById("id_old_password");
    const password2Input = document.getElementById("id_new_password1");
    const password3Input = document.getElementById("id_new_password2");
    const passwordToggle1 = document.getElementById("toogle-pass-1");
    const passwordToggle2 = document.getElementById("toogle-pass-2");
    const passwordToggle3 = document.getElementById("toogle-pass-3");

    // Manejador devents mostrar password1
    passwordToggle1.addEventListener("click",function(){
      if (password1Input.type==="password"){
        password1Input.type = "text";
        this.innerHTML = '<i class="fas fa-eye-slash" title="Ocultar contraseña" style="cursor: pointer;"></i>';
      }else if(password1Input.type==="text"){
        password1Input.type = "password";
        this.innerHTML = '<i class="fas fa-eye" title="Ver contraseña" style="cursor: pointer;"></i>';
      }
    })

    // Manejador devents mostrar password2
    passwordToggle2.addEventListener("click",function(){
      if (password2Input.type==="password"){
        password2Input.type = "text";
        this.innerHTML = '<i class="fas fa-eye-slash" title="Ocultar contraseña" style="cursor: pointer;"></i>';
      }else if(password2Input.type==="text"){
        password2Input.type = "password";
        this.innerHTML = '<i class="fas fa-eye" title="Ver contraseña" style="cursor: pointer;"></i>';
      }
    })

    // Manejador devents mostrar password3
    passwordToggle3.addEventListener("click",function(){
        if (password3Input.type==="password"){
          password3Input.type = "text";
          this.innerHTML = '<i class="fas fa-eye-slash" title="Ocultar contraseña" style="cursor: pointer;"></i>';
        }else if(password3Input.type==="text"){
          password3Input.type = "password";
          this.innerHTML = '<i class="fas fa-eye" title="Ver contraseña" style="cursor: pointer;"></i>';
        }
      })



  });