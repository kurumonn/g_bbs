window.addEventListener("load" , function (){ 



    $("#sample3check").on("change", function(){
          if ($(this).prop("checked")) {
            // ダークモード
            document.body.classList.remove("light-theme");
            document.body.classList.add("dark-theme");
                                             
          } else {
            // ライトモード
            document.body.classList.remove("dark-theme");
            document.body.classList.add("light-theme");
         
          }   
            
    }); 
});

