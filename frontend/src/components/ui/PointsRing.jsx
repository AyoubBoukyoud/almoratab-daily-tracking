import { motion } from 'framer-motion';

const RADIUS = 90;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // ≈ 565.5

export function PointsRing({ current, max = 400, sprintInfo }) {
  const percentage = Math.min(current / max, 1);
  const strokeDashoffset = CIRCUMFERENCE * (1 - percentage);

  return (
    <div className="flex flex-col items-center py-8">
      <div className="relative">
        <svg width="220" height="220" viewBox="0 0 220 220">
          {/* Background track */}
          <circle
            cx="110" cy="110" r={RADIUS}
            fill="none"
            stroke="#1A4D4A"
            strokeWidth="14"
            className="opacity-10"
          />
          {/* Animated progress arc */}
          <motion.circle
            cx="110" cy="110" r={RADIUS}
            fill="none"
            stroke="#C9982A"
            strokeWidth="14"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            initial={{ strokeDashoffset: CIRCUMFERENCE }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.4, ease: "easeOut" }}
            style={{ transform: 'rotate(-90deg)', transformOrigin: '110px 110px' }}
          />
          {/* Center text */}
          <text x="110" y="100" textAnchor="middle"
            className="font-bold" fontSize="36" fill="#1A4D4A">
            {current}
          </text>
          <text x="110" y="124" textAnchor="middle"
            fontSize="14" fill="#6B8280">
            / {max} pts
          </text>
        </svg>
      </div>
      {sprintInfo && (
        <p className="text-brand-teal text-sm mt-2 font-medium">
          {sprintInfo.name} · Day {sprintInfo.currentDay}
        </p>
      )}
    </div>
  );
}
