import logo from "../assets/LOGOCV.png";

export default function Alerts() {

  const data = [
    { type: "Drowsiness", time: "10:23 AM", desc: "Eyes closed for 3.2 seconds" },
    { type: "Face Direction", time: "9:50 AM", desc: "Looking left for too long" },
    { type: "Phone Usage", time: "9:30 AM", desc: "Detected phone in hand" },
  ];

  return (
    <div className="min-h-screen bg-[#F5F9FF] px-6 py-6">

      <div className="flex items-center gap-3 mb-6">
        <img src={logo} className="w-10 h-10" />
        <h1 className="text-xl font-bold text-blue-600">Alerts & History</h1>
      </div>

      {data.map((a, i) => (
        <div
          key={i}
          className="bg-white p-4 rounded-xl shadow border border-gray-200 mb-4"
        >
          <h3 className="text-lg font-semibold text-red-500">{a.type}</h3>
          <p className="text-gray-700">{a.desc}</p>
          <p className="text-gray-500 text-sm mt-1">{a.time}</p>
        </div>
      ))}

    </div>
  );
}
