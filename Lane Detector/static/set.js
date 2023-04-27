function validateForm() {
    let x = document.forms["new_user_form"]["username"].value;
    if (x==""){
      alert("Must fill out username");
      return false
    } else if (x.includes("\"")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes("(")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(")")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(".")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(",")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes("{")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes("}")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(":")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(";")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes("<")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes(">")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
    } else if (x.includes("\'")){
      alert("Do not include characters: \".,(){}:;<>\'");
      return false
   
  }
  
  let y = document.forms["new_user_form"]["password"].value;
  if (y==""){
    alert("Must fill out password");
    return false
  } else if (y.includes("\"")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes("(")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(")")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(".")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(",")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes("{")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes("}")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(":")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(";")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes("<")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes(">")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  } else if (y.includes("\'")){
    alert("Do not include characters: \".,(){}:;<>\'");
    return false
  
  }
  
  }
  
  