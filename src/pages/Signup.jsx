import { useState } from "react";
import logo from "../assets/LOGOCV.png";

export default function Signup() {
  const [f, setF] = useState({
    name: "",
    age: "",
    gender: "",
    phone: "",
    emergencyName: "",
    emergencyPhone: "",
    password: "",
  });

  async function signup() {
    try {
      const res = await fetch("http://localhost:3000/api/v1/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: f.name,
          age: f.age,
          gender: f.gender.toLowerCase(),
          phone: f.phone,
          emergencyname: f.emergencyName,
          emergencyphone: f.emergencyPhone,
          password: f.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.message || "Signup failed");
        return;
      }

      alert("Signup successful 🎉");
      window.location.href = "/login"; // navigate after success

    } catch (err) {
      alert("Server error. Try again later.");
      console.error(err);
    }
  }
  return (
    <div className="min-h-screen bg-[#F5F9FF] flex justify-center items-center px-6">

      <div className="bg-white p-8 rounded-3xl shadow-xl w-full max-w-md border border-blue-100">

        <img src={logo} className="w-24 h-24 mx-auto mb-6" />

        <h2 className="text-2xl font-bold text-blue-600 text-center mb-6">
          Create Account
        </h2>

        {[
          ["name", "Name"],
          ["age", "Age"],
          ["phone", "Phone Number"],
          ["emergencyName", "Emergency Contact Name"],
          ["emergencyPhone", "Emergency Contact Number"],
          ["password", "Password"],
        ].map(([key, label]) => (
          <input
            key={key}
            placeholder={label}
            type={key === "password" ? "password" : "text"}
            className="w-full p-3 border rounded-xl mb-4 shadow-sm border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
            onChange={(e) => setF({ ...f, [key]: e.target.value })}
          />
        ))}

        <select
          value={f.gender}
          onChange={(e) => setF({ ...f, gender: e.target.value })}
          className="w-full p-3 border rounded-xl mb-4 shadow-sm border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="">Select Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>


        <button
          onClick={signup}
          className="w-full bg-blue-600 text-white py-3 rounded-xl shadow hover:bg-blue-700 active:scale-95"
        >
          Sign Up
        </button>

      </div>
    </div>
  );
}

