import { useEffect, useState } from "react";
import logo from "../assets/LOGOCV.png";

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Not authenticated");
      setLoading(false);
      return;
    }

    fetch("http://localhost:3000/api/v1/profile", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.message || "Failed to fetch profile");
        }
        return res.json();
      })
      .then((data) => {
        setProfile(data);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6 text-blue-600">Loading profile...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-[#F5F9FF] px-6 py-6">
      <div className="flex items-center gap-3 mb-6">
        <img src={logo} className="w-10 h-10" />
        <h1 className="text-2xl font-bold text-blue-600">Dashboard</h1>
      </div>

      {/* Profile */}
      <div className="bg-white p-6 rounded-2xl shadow border border-blue-100 mb-6">
        <h2 className="text-xl font-bold text-blue-700 mb-2">Profile</h2>

        <p><b>Name:</b> {profile.username}</p>
        <p><b>Age:</b> {profile.age}</p>
        <p><b>Gender:</b> {profile.gender}</p>
        <p><b>Phone:</b> {profile.phone}</p>
        <p>
          <b>Emergency:</b> {profile.emergencyname} – {profile.emergencyphone}
        </p>

        <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold hover:bg-blue-700">
          Edit Profile
        </button>
      </div>

      {/* Emergency Contacts */}
      <div className="bg-white p-6 rounded-2xl shadow border border-blue-100">
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Emergency Contacts
        </h2>

        <p className="text-gray-700">
          {profile.emergencyname} – {profile.emergencyphone}
        </p>

        <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold hover:bg-blue-700">
          Add Contact
        </button>
      </div>
    </div>
  );
}
