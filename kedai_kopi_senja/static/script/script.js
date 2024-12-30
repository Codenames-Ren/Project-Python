//Pilihan Menu-->
let totalHargaMakanan = 0;
let cart = [];
let pembelian = [];

function debug() {
  console.log(pembelian);
}

async function orderFood() {
  if (checkAvailable()) {
    try {
      const updateStockPayload = cart.map((item) => ({
        name: item.name,
        jumlah: item.jumlah,
      }));

      console.log(
        "Payload yang dikirim:",
        JSON.stringify({ orders: updateStockPayload })
      );

      const response = await fetch("/api/update_stock", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cart: updateStockPayload }),
      });

      const result = await response.json();
      console.log("Response dari server:", result);

      if (result.message === "success") {
        // Perbarui stok secara lokal
        for (let item of cart) {
          const menu = food.find((menuItem) => menuItem.name === item.name);
          if (menu) {
            menu.stok -= item.jumlah;
          }
        }

        alert(
          `Pesanan telah diterima! Total Harga: Rp${toRupiah(
            totalHargaMakanan
          )},00`
        );

        pembelian.push([...cart]);
        cart = [];
        totalHargaMakanan = 0;

        fetchMenu();
        generateData();
      } else {
        console.error("Gagal memperbarui stok:", result.error);
        alert("Gagal memperbarui stok: " + result.error);
      }
    } catch (error) {
      console.error("Terjadi kesalahan:", error);
      alert("Terjadi kesalahan saat memproses pesanan.");
    }
  }
}

function checkAvailable() {
  for (let item of cart) {
    const menu = food.find((menuItem) => menuItem.name === item.name);
    if (!menu || menu.stok < item.jumlah) {
      alert(
        `Stok ${menu ? menu.name : item.name} tinggal ${menu ? menu.stok : 0}`
      );
      return false;
    }
  }
  return true;
}

function addtoCart(index) {
  console.log(food[index].name);
  var hasExist = false;
  var hasEmpty = false;
  if (food[index].stok <= 0) {
    alert(`${food[index].name} habis, silahkan pesan menu lainnya`);
    hasEmpty = true;
  }
  for (var i = 0; i < cart.length; i++) {
    if (food[index].name === cart[i].name) {
      if (food[index].stok - cart[i].jumlah <= 0) {
        alert(`${food[index].name} habis, silahkan pesan menu lainnya`);
        hasEmpty = true;
        break;
      } else {
        totalHargaMakanan += cart[i].harga;
        //console.log(totalHargaMakanan);
        cart[i].jumlah++;
        hasExist = true;
        break;
      }
    }
  }
  if (!hasExist && !hasEmpty) {
    let obj = {
      name: food[index].name,
      harga: food[index].harga,
      jumlah: 1,
      image: food[index].image,
    };
    totalHargaMakanan += food[index].harga;
    cart.push(obj);
  }
  generateData();
  var cartlist = document.getElementById("cartList");
  if (cart.length !== 0) {
    cartlist.setAttribute("style", "display:inline-block");
  }
}

function removeFood(value) {
  //console.log(cart[value].jumlah);
  if (cart[value].jumlah > 0) {
    totalHargaMakanan -= cart[value].harga;
    cart[value].jumlah--;
  }
  if (cart[value].jumlah === 0) {
    cart.splice(value, 1);
  }
  generateData();
  var cartlist = document.getElementById("cartList");
  if (cart.length !== 0) {
    cartlist.setAttribute("style", "display:inline-block");
  } else {
    // UNTUK MATIKAN CARTLIST

    cartlist.setAttribute("style", "display:none");
  }
}

function toRupiah(harga) {
  var result = "";
  harga = String(harga);
  var arr = [];
  var count = 0;
  for (var i = harga.length - 1; i >= 0; i--) {
    if (count === 3 && harga[i] != undefined) {
      arr.push(".");
      arr.push(harga[i]);
      count = 1;
      // console.log(count,i,'MASUK');
    } else {
      arr.push(harga[i]);
      count++;
      //console.log(count,i-1);
    }
  }
  //console.log(arr);
  for (var i = arr.length - 1; i >= 0; i--) {
    result += arr[i];
  }
  return result;
}

// Ini fungsi terakhir di dalam script.js Anda
async function fetchMenu() {
  try {
    const response = await fetch("/api/get_menu"); // Sesuaikan endpoint dengan backend Anda
    const result = await response.json();

    if (result.menu) {
      food = result.menu; // Update variabel food hanya jika API berhasil
      console.log("Menu berhasil diambil:", food);
      generateData(); // Perbarui tampilan
    } else {
      throw new Error("Format respons tidak sesuai");
    }
  } catch (error) {
    console.error("Error saat mengambil data menu:", error);
    alert("Gagal mengambil menu. Silakan coba lagi nanti.");
  }
}

//console.log(toRupiah(1910450));

function generateData() {
  const foodList = document.getElementById("foodList");
  const cartList = document.getElementById("cartList");
  foodList.innerHTML = "";
  cartList.innerHTML = "";

  for (var i = 0; i < food.length; i++) {
    let name = food[i].name;
    let stok = food[i].stok;
    let harga = food[i].harga;
    let image = food[i].image;

    let divCard = document.createElement("div");
    divCard.classList.add("card");

    let imageData = document.createElement("img");
    imageData.setAttribute("src", image);
    divCard.appendChild(imageData);

    let title = document.createElement("p");
    title.innerHTML = name;
    divCard.appendChild(title);

    let divAction = document.createElement("div");
    divAction.classList.add("action");

    let spanData = document.createElement("span");
    spanData.innerHTML = `Rp ${toRupiah(harga)},00 | Stok : ${stok}`;
    divAction.appendChild(spanData);

    let buttonAdd = document.createElement("button");
    buttonAdd.innerHTML = '<i class="fas fa-cart-plus"></i> Pesan';
    buttonAdd.setAttribute("value", i);
    buttonAdd.setAttribute("onclick", "addtoCart(this.value)");
    divAction.appendChild(buttonAdd);
    divCard.appendChild(divAction);
    //console.log(divCard);
    foodList.appendChild(divCard);
  }

  let totalDiv = document.createElement("div");
  totalDiv.classList.add("total");

  let totalh1 = document.createElement("h1");
  totalh1.innerHTML = `TOTAL : Rp${toRupiah(totalHargaMakanan)},00`;
  totalDiv.appendChild(totalh1);

  let totalhr = document.createElement("hr");
  totalDiv.appendChild(totalhr);
  //console.log(totalDiv);
  cartList.appendChild(totalDiv);

  //console.log('BelumMasuk');
  for (var x = 0; x < cart.length; x++) {
    let name = cart[x].name;
    let jumlah = cart[x].jumlah;
    let harga = cart[x].harga;
    let image = cart[x].image;
    //console.log('MASUK');
    let divCardx = document.createElement("div");
    divCardx.classList.add("card-order");
    //console.log(divCardx);

    let divCardDetail = document.createElement("div");
    divCardDetail.classList.add("detail");

    let imageData = document.createElement("img");
    imageData.setAttribute("src", image);
    divCardDetail.appendChild(imageData);

    let foodName = document.createElement("p");
    // foodName.setAttribute('id','nameCart')
    foodName.innerHTML = name;
    divCardDetail.appendChild(foodName);

    let foodJumlah = document.createElement("span");
    foodJumlah.innerHTML = jumlah;
    divCardDetail.appendChild(foodJumlah);

    divCardx.appendChild(divCardDetail);

    let buttonCancel = document.createElement("button");
    buttonCancel.setAttribute("value", x);
    buttonCancel.setAttribute("id", "cancelCart");
    buttonCancel.setAttribute("onclick", "removeFood(this.value)");
    buttonCancel.innerHTML = '<i class="fas fa-trash"></i> Hapus';
    divCardx.appendChild(buttonCancel);
    //console.log(divCardx);

    cartList.appendChild(divCardx);
  }

  let divbutton = document.createElement("div");
  divbutton.classList.add("card-finish");

  let buttonOrder = document.createElement("button");
  //buttonOrder.classList.add('order');
  buttonOrder.setAttribute("onclick", "orderFood()");
  buttonOrder.innerHTML = "ORDER SEKARANG";
  divbutton.appendChild(buttonOrder);
  cartList.appendChild(divbutton);
}

generateData();
fetchMenu();
