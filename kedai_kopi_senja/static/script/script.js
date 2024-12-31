//Pilihan Menu-->
let totalHargaMakanan = 0;
let cart = [];
let pembelian = [];

let food = [];

// Fetch data menu dari server
fetch("/api/menu")
  .then((response) => response.json())
  .then((data) => {
    food = data.menu; // Simpan data menu ke variabel food
    console.log("Data menu:", food);
  })
  .catch((error) => console.error("Error fetching menu data:", error));

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
      console.log("Response dari API:", result);
      console.log("Data menu setelah di fetch:", food);

      if (result.message === "Success") {
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

        const cartlist = document.getElementById("cartList");
        cartlist.setAttribute("style", "display:none");

        fetchMenu();
        generateData();
      } else {
        console.log("Gagal memperbarui stok:", result); // Tambahkan logging
        // console.error("Gagal memperbarui stok:", result.error);
        alert("Gagal memperbarui stok: " + (result.error || "Unknown Error"));
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

  if (food[index].stock <= 0) {
    alert(`${food[index].name} habis, silahkan pesan menu lainnya`);
    return;
  }

  const existingItem = cart.find((item) => item.name === food[index].name);
  if (existingItem) {
    if (food[index].stock - existingItem.jumlah <= 0) {
      alert(`${food[index].name} habis, silahkan pesan menu lainnya`);
      return;
    }
    existingItem.jumlah++;
    totalHargaMakanan += existingItem.harga; // Menggunakan "harga" dari cart
  } else {
    cart.push({
      name: food[index].name,
      harga: food[index].price, // Pastikan ini sesuai dengan field API
      jumlah: 1,
      image: food[index].image,
    });
    totalHargaMakanan += food[index].price;
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
    const response = await fetch("/api/menu");
    const rawData = await response.json();

    console.log("Data mentah dari API:", rawData);

    if (!rawData.menu || !Array.isArray(rawData.menu)) {
      throw new TypeError(
        "Data menu yang diterima tidak valid atau bukan array."
      );
    }

    food = rawData.menu; // Akses array menu
    console.log("Data menu yang diakses:", food);
    generateData();
  } catch (error) {
    console.error("Gagal mengambil menu:", error);
    alert("Kesalahan: " + error.message);
  }
}

//console.log(toRupiah(1910450));

function generateData() {
  console.log("Memulai generate data...");
  console.log("Isi food sebelum generate:", food);
  // console.log("Isi cart sebelum generate:", cart);
  console.log("Isi cart untuk perhitungan:", cart);
  cart.forEach((item) => {
    if (isNaN(item.harga) || isNaN(item.jumlah)) {
      console.error("Item tidak valid:", item);
    }
  });

  // Hitung ulang total harga
  totalHargaMakanan = cart.reduce(
    (total, item) => total + item.harga * item.jumlah,
    0
  );
  console.log("Total harga dihitung ulang:", totalHargaMakanan);

  const foodList = document.getElementById("foodList");
  const cartList = document.getElementById("cartList");

  foodList.innerHTML = "";
  cartList.innerHTML = "";

  food.forEach((item, index) => {
    // Buat card makanan
    let divCard = document.createElement("div");
    divCard.classList.add("card");

    let imageData = document.createElement("img");
    imageData.setAttribute("src", item.image);
    divCard.appendChild(imageData);

    let title = document.createElement("p");
    title.innerHTML = item.name;
    divCard.appendChild(title);

    let divAction = document.createElement("div");
    divAction.classList.add("action");

    let spanData = document.createElement("span");
    spanData.innerHTML = `Rp ${toRupiah(item.price)},00 | Stok : ${item.stock}`;
    divAction.appendChild(spanData);

    let buttonAdd = document.createElement("button");
    buttonAdd.innerHTML = '<i class="fas fa-cart-plus"></i> Pesan';
    buttonAdd.setAttribute("value", index);
    buttonAdd.setAttribute("onclick", "addtoCart(this.value)");
    divAction.appendChild(buttonAdd);
    divCard.appendChild(divAction);

    foodList.appendChild(divCard);
  });

  // Buat elemen total harga
  let totalDiv = document.createElement("div");
  totalDiv.classList.add("total");

  let totalh1 = document.createElement("h1");
  totalh1.innerHTML = `TOTAL : Rp${toRupiah(totalHargaMakanan)},00`;
  totalDiv.appendChild(totalh1);

  let totalhr = document.createElement("hr");
  totalDiv.appendChild(totalhr);
  cartList.appendChild(totalDiv);

  cart.forEach((item, index) => {
    let divCardx = document.createElement("div");
    divCardx.classList.add("card-order");

    let divCardDetail = document.createElement("div");
    divCardDetail.classList.add("detail");

    let imageData = document.createElement("img");
    imageData.setAttribute("src", item.image);
    divCardDetail.appendChild(imageData);

    let foodName = document.createElement("p");
    foodName.innerHTML = item.name;
    divCardDetail.appendChild(foodName);

    let foodJumlah = document.createElement("span");
    foodJumlah.innerHTML = item.jumlah;
    divCardDetail.appendChild(foodJumlah);

    divCardx.appendChild(divCardDetail);

    let buttonCancel = document.createElement("button");
    buttonCancel.setAttribute("value", index);
    buttonCancel.setAttribute("onclick", "removeFood(this.value)");
    buttonCancel.innerHTML = '<i class="fas fa-trash"></i> Hapus';
    divCardx.appendChild(buttonCancel);

    cartList.appendChild(divCardx);
  });

  let divbutton = document.createElement("div");
  divbutton.classList.add("card-finish");

  let buttonOrder = document.createElement("button");
  buttonOrder.setAttribute("onclick", "orderFood()");
  buttonOrder.innerHTML = "ORDER SEKARANG";
  divbutton.appendChild(buttonOrder);
  cartList.appendChild(divbutton);
}

generateData();
fetchMenu();
