import { useState, useEffect, useRef } from "react";
import logo from "../assets/LOGOCV.png";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
const CAPTURE_INTERVAL_MS = 200;
const ML_HELP = "Start the ml (see ml/README.md): uvicorn ml.ml_server:app --port 8000";

export default function Monitor() {
  const [time, setTime] = useState("");
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [stream, setStream] = useState(null);
  const [eyeStatus, setEyeStatus] = useState("—");
  const [faceDirection, setFaceDirection] = useState("—");
  const [yawnStatus, setYawnStatus] = useState("—");
  const [earVal, setEarVal] = useState("—");
  const [marVal, setMarVal] = useState("—");
  const [error, setError] = useState(null);
  const [apiError, setApiError] = useState(null);
  const [yawnLatched, setYawnLatched] = useState(false);
  const yawnTimeoutRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const loopRef = useRef(null);
  const sendingRef = useRef(false);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setTime(
        now.toLocaleTimeString("en-US", {
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    return () => {
      if (loopRef.current) clearInterval(loopRef.current);
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, [stream]);

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  const startMonitoring = async () => {
    setError(null);
    setApiError(null);
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
      });
      setStream(mediaStream);
      setIsMonitoring(true);
    } catch (e) {
      setError("Could not access camera. Please allow camera access.");
    }
  };

  const handleStop = () => {
    if (loopRef.current) {
      clearInterval(loopRef.current);
      loopRef.current = null;
    }

    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      setStream(null);
    }

    if (videoRef.current) videoRef.current.srcObject = null;

    // 🔥 ADD THIS (yawn cleanup)
    if (yawnTimeoutRef.current) {
      clearTimeout(yawnTimeoutRef.current);
      yawnTimeoutRef.current = null;
    }
    setYawnLatched(false);
    setYawnStatus("—");

    setIsMonitoring(false);
  };


  useEffect(() => {
    if (!isMonitoring || !stream) return;

    const sendFrame = async () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (!video || !canvas) return;
      if (video.readyState !== video.HAVE_ENOUGH_DATA) return;
      if (video.videoWidth <= 0 || video.videoHeight <= 0) return;
      if (sendingRef.current) return;

      sendingRef.current = true;
      const ctx = canvas.getContext("2d");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);

      const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.95));
      if (!blob) {
        sendingRef.current = false;
        return;
      }

      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      try {
        const res = await fetch(`${API_BASE}/api/detect`, { method: "POST", body: formData });
        let data = {};
        try {
          data = await res.json();
        } catch (_) { /* ignore */ }
        if (!res.ok) throw new Error((data && data.detail) || res.statusText || "Request failed");

        setApiError(null);
        setEyeStatus(data.drowsiness?.eye_status === "closed" ? "Closed" : "Open");
        if (data.drowsiness?.yawn_detected) {
          setYawnLatched(true);
          setYawnStatus("Yawning");

          if (yawnTimeoutRef.current) {
            clearTimeout(yawnTimeoutRef.current);
            
          }

          yawnTimeoutRef.current = setTimeout(() => {
            setYawnLatched(false);
            setYawnStatus("Normal");
          }, 2000); // 👈 visible for 2 seconds
        }
        else if (!yawnLatched) {
          setYawnStatus("Normal");
        }


        setEarVal(data.drowsiness?.ear);
        setMarVal(data.drowsiness?.mar);
        setFaceDirection(data.distraction?.distracted ? "Looking away" : "Forward");
      } catch (err) {
        const isNetworkError = !err.message || err.message === "Failed to fetch";
        const message = isNetworkError ? `Cannot connect to ${API_BASE}. ${ML_HELP}` : err.message;
        setApiError(message);
        setEyeStatus("—");
        setYawnStatus("—");
        setEarVal("—");
        setMarVal("—");
        setFaceDirection("—");
      } finally {
        sendingRef.current = false;
      }
    };

    sendFrame();
    loopRef.current = setInterval(sendFrame, CAPTURE_INTERVAL_MS);

    return () => {
      if (loopRef.current) {
        clearInterval(loopRef.current);
        loopRef.current = null;
      }
    };
  }, [isMonitoring, stream]);

  return (
    <div className="min-h-screen bg-white px-6 pt-4 flex flex-col">
      <div className="flex items-center justify-between py-3">
        <div className="flex items-center gap-2">
          <img src={logo} className="w-8 h-8 rounded-md" alt="logo" />
          <h1 className="text-xl font-semibold text-blue-600">VisionCam</h1>
        </div>
        <div className="flex items-center gap-4 text-gray-600">
          <span className="font-medium">{time}</span>
          <span className="text-xl">⚙️</span>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-100 shadow-inner rounded-2xl flex flex-col items-center justify-center h-[420px] mt-4 overflow-hidden relative">
        {isMonitoring && stream ? (
          <>
            <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-contain bg-black" />
            <canvas ref={canvasRef} className="hidden" />
          </>
        ) : (
          <>
            <span className="text-5xl text-blue-300">👁️</span>
            <p className="text-gray-700 font-medium mt-2">Camera Preview</p>
            <p className="text-gray-400 text-sm">Press Start to begin monitoring</p>
          </>
        )}
      </div>

      {error && <p className="mt-2 text-red-600 text-sm text-center">{error}</p>}
      {apiError && <p className="mt-2 text-amber-600 text-sm text-center">API: {apiError}</p>}

      <div className="grid grid-cols-3 gap-4 mt-6">
        {/* Eye Status */}
        <div className="bg-white shadow-md rounded-xl py-4 flex flex-col items-center">
          <span className="text-2xl text-green-500">👁️</span>
          <p className="text-gray-600 text-sm mt-1">Eye Status</p>
          <p className={`text-sm font-semibold mt-1 ${eyeStatus === "Closed" ? "text-amber-600" : "text-green-600"}`}>
            {eyeStatus}
          </p>
        </div>

        {/* Face Direction */}
        <div className="bg-white shadow-md rounded-xl py-4 flex flex-col items-center">
          <span className="text-2xl text-blue-500">➡️</span>
          <p className="text-gray-600 text-sm mt-1">Face Direction</p>
          <p className={`text-sm font-semibold mt-1 ${faceDirection === "Looking away" ? "text-amber-600" : "text-blue-600"}`}>
            {faceDirection}
          </p>
        </div>

        {/* Yawning */}
        <div className="bg-white shadow-md rounded-xl py-4 flex flex-col items-center">
          <span className="text-2xl text-amber-500">😮</span>
          <p className="text-gray-600 text-sm mt-1">Yawning</p>
          <p className={`text-sm font-semibold mt-1 ${yawnStatus === "Yawning" ? "text-red-600" : "text-green-600"}`}>
            {yawnStatus}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            MAR: {typeof marVal === "number" ? marVal.toFixed(3) : marVal} &nbsp;
            EAR: {typeof earVal === "number" ? earVal.toFixed(3) : earVal}
          </p>
        </div>
      </div>

      {!isMonitoring ? (
        <button type="button" onClick={startMonitoring} className="mt-6 bg-blue-600 hover:bg-blue-700 text-white w-full py-4 rounded-xl shadow-lg font-semibold">
          Start Monitoring
        </button>
      ) : (
        <button type="button" onClick={handleStop} className="mt-6 bg-red-600 hover:bg-red-700 text-white w-full py-4 rounded-xl shadow-lg font-semibold">
          Stop Monitoring
        </button>
      )}

      <div className="mt-4 text-center space-y-2">
        <a href="/alerts" className="text-blue-500 text-sm underline block">View Alerts & History</a>
        <a href="/dashboard" className="text-blue-500 text-sm underline block">Go to Dashboard</a>
      </div>
    </div>
  );
}