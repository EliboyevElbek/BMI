fetch("http://127.0.0.1:8000/api/v1/categories")
  .then(res => {
    if (!res.ok) {
      throw new Error("Serverdan noto‘g‘ri javob keldi: " + res.status);
    }
    return res.json(); // JSON ga aylantirish
  })
  .then(data => {
    console.log("Kelgan ma'lumot:", data); // Bu yerda ma'lumot
  })
  .catch(err => {
    console.error("Xatolik:", err);
  });
