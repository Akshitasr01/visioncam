export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-between bg-gray-50 pb-10">

      {/* Top Curve */}
      <div className="w-full h-10 bg-gray-900 rounded-b-3xl"></div>

      {/* Logo + Title */}
      <div className="flex flex-col items-center mt-10 px-6">
        <div className="w-40 h-40 bg-white shadow-xl rounded-2xl flex items-center justify-center border">
          <img
            src="/src/assets/LOGOCV.png"
            alt="VisionCam Logo"
            className="w-28 h-28 object-contain"
          />
        </div>

        <h1 className="text-4xl font-extrabold text-blue-600 mt-6">
          VisionCam
        </h1>

        <p className="text-gray-600 text-center mt-2 text-md">
          Prevent accidents before they happen
        </p>
      </div>

      {/* Features */}
      <div className="w-full max-w-md mt-8 space-y-4 px-10">
        <p className="flex items-center gap-3 text-blue-600 text-lg">
          <span className="text-blue-500 text-2xl">•</span>
          Real-time drowsiness detection
        </p>

        <p className="flex items-center gap-3 text-blue-600 text-lg">
          <span className="text-blue-500 text-2xl">•</span>
          Face direction monitoring
        </p>

        <p className="flex items-center gap-3 text-blue-600 text-lg">
          <span className="text-blue-500 text-2xl">•</span>
          Phone usage alerts
        </p>
      </div>

      {/* BUTTONS */}
      <div className="w-full flex flex-col items-center mt-10 space-y-4">

        <a
          href="/monitor"
          className="w-80 bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold py-4 rounded-xl shadow-lg text-center transition"
        >
          Start Monitoring
        </a>

        <a
          href="/dashboard"
          className="w-80 bg-gray-800 hover:bg-gray-900 text-white text-md font-semibold py-3 rounded-xl shadow-md text-center transition"
        >
          View Dashboard
        </a>

      </div>
    </div>
  );
}
