import { useState } from "react";
import logo from "../assets/LOGOCV.png";

export default function Alerts() {
  const [alerts] = useState([
    { id: 1, type: "Drowsiness Detected", time: "10:12:45", status: "Critical", icon: "😴" },
    { id: 2, type: "Phone Usage", time: "09:48:10", status: "Warning", icon: "📱" },
    { id: 3, type: "Looked Away", time: "09:15:22", status: "Warning", icon: "👀" },
  ]);

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-4">

      {/* NAVBAR */}
      <div className="flex items-center justify-between py-3">
        <div className="flex items-center gap-2">
          <img src={logo} className="w-8 h-8 rounded-md" alt="logo" />
          <h1 className="text-xl font-semibold text-blue-600">VisionCam</h1>
        </div>

        <a href="/monitor" className="text-blue-600 font-semibold text-sm underline">
          Back
        </a>
      </div>

      <h2 className="text-2xl font-bold text-gray-800 mt-4">Alerts & History</h2>
      <p className="text-gray-500 mb-4">Recent detections from the monitoring</p>

      {/* ALERT LIST */}
      <div className="space-y-4">
        {alerts.map((alert) => (
          <div
            key={alert.id}
            className="bg-white shadow-md rounded-xl p-4 flex items-center justify-between border border-gray-100"
          >
            <div className="flex items-center gap-4">
              <span className="text-3xl">{alert.icon}</span>
              <div>
                <p className="font-semibold text-gray-700">{alert.type}</p>
                <p className="text-gray-400 text-sm">{alert.time}</p>
              </div>
            </div>

            <span
              className={`px-3 py-1 text-sm rounded-lg font-semibold
                ${alert.status === "Critical" ? "bg-red-100 text-red-600" : "bg-yellow-100 text-yellow-600"}`}
            >
              {alert.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
