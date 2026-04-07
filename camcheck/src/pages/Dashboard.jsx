import logo from "../assets/LOGOCV.png";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 px-6 py-4">

      {/* NAVBAR */}
      <div className="flex items-center justify-between py-3">
        <div className="flex items-center gap-2">
          <img src={logo} className="w-8 h-8 rounded-md" alt="logo" />
          <h1 className="text-xl font-semibold text-blue-600">VisionCam</h1>
        </div>

        <a href="/" className="text-blue-600 font-semibold text-sm underline">
          Home
        </a>
      </div>

      <h2 className="text-3xl font-bold text-gray-800 mt-4">Dashboard</h2>
      <p className="text-gray-500 mb-6">Driver safety insights</p>

      {/* STATS */}
      <div className="grid grid-cols-2 gap-4">

        <div className="bg-white p-5 rounded-xl shadow-md flex flex-col items-center">
          <span className="text-4xl">🚨</span>
          <p className="text-gray-600 mt-2">Total Alerts</p>
          <p className="text-2xl font-bold text-blue-600">14</p>
        </div>

        <div className="bg-white p-5 rounded-xl shadow-md flex flex-col items-center">
          <span className="text-4xl">😴</span>
          <p className="text-gray-600 mt-2">Drowsiness</p>
          <p className="text-2xl font-bold text-red-500">5</p>
        </div>

        <div className="bg-white p-5 rounded-xl shadow-md flex flex-col items-center">
          <span className="text-4xl">📱</span>
          <p className="text-gray-600 mt-2">Phone Distractions</p>
          <p className="text-2xl font-bold text-yellow-500">6</p>
        </div>

        <div className="bg-white p-5 rounded-xl shadow-md flex flex-col items-center">
          <span className="text-4xl">👀</span>
          <p className="text-gray-600 mt-2">Off-road Glances</p>
          <p className="text-2xl font-bold text-purple-500">3</p>
        </div>

      </div>

      {/* SUMMARY */}
      <div className="bg-white mt-8 p-5 rounded-xl shadow-md">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Summary</h3>

        <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
          <div className="h-full bg-red-400 w-[35%]"></div>
        </div>

        <p className="text-sm text-gray-500 mt-2">
          High alert activity detected today.
        </p>

        <div className="mt-4 space-y-2">
          <a href="/monitor" className="text-blue-500 underline block">
            Go to Monitor
          </a>

          <a href="/alerts" className="text-blue-500 underline block">
            View Alerts
          </a>
        </div>
      </div>

    </div>
  );
}
