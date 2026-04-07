import logo from "../assets/LOGOCV.png";

export default function Settings() {
  return (
    <div className="min-h-screen bg-white px-6 py-6">

      <div className="flex items-center gap-3 mb-8">
        <img src={logo} className="w-10 h-10" />
        <h1 className="text-2xl font-bold text-blue-600">Settings</h1>
      </div>

      <div className="space-y-4">

        <button
          onClick={() => (window.location.href = "/alerts")}
          className="w-full bg-white p-4 rounded-xl border shadow text-left font-semibold text-gray-700 hover:bg-blue-50"
        >
          Alerts & History
        </button>

        <button
          onClick={() => (window.location.href = "/dashboard")}
          className="w-full bg-white p-4 rounded-xl border shadow text-left font-semibold text-gray-700 hover:bg-blue-50"
        >
          Dashboard
        </button>

        <button
          onClick={() => (window.location.href = "/")}
          className="w-full bg-white p-4 rounded-xl border shadow text-left font-semibold text-red-500 hover:bg-red-50"
        >
          Logout
        </button>

      </div>

    </div>
  );
}
