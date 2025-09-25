import React from "react";
import { useSuperTicTacToe } from "../SuperTicTacToeContext";

type Player = "X" | "O";
type Cell = Player | null;

type Props = {
  subGameIndex: number;
  onSubGameEnd: (result: Player | "draw") => void;
  onMoveMade: (cellIndex: number) => void;
  disabled?: boolean;
};

// ----- Backend DTOs -----
type GameStateDTO = {
  id: string;
  board: Cell[];
  current_player: Player;
  winner: Player | null;
  is_draw: boolean;
  status: string;
};

// Prefer env, fallback to localhost:8000
const API_BASE =
  (import.meta as any)?.env?.VITE_API_URL?.replace(/\/$/, "") ??
  "http://localhost:8000";



export default function TicTacToe({ subGameIndex, onSubGameEnd, onMoveMade, disabled = false }: Props) {
  const { currentPlayer, legalBoards, switchPlayer } = useSuperTicTacToe();
  const [state, setState] = React.useState<GameStateDTO | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  // Create a new game on mount
  React.useEffect(() => {
    let canceled = false;
    async function start() {
      setError(null);
      setLoading(true);
      try {
        const gs = await createGame();
        if (!canceled) setState(gs);
      } catch (e: any) {
        if (!canceled) setError(e?.message ?? "Failed to start game");
      } finally {
        if (!canceled) setLoading(false);
      }
    }
    start();
    return () => {
      canceled = true;
    };
  }, []);

  // Notify parent when result changes
  React.useEffect(() => {
    if (!state) return;
    if (state.winner) onSubGameEnd(state.winner);
    else if (state.is_draw) onSubGameEnd("draw");
  }, [state?.winner, state?.is_draw, onSubGameEnd]);

  const isPlayable = legalBoards.includes(subGameIndex);

  async function createGame(): Promise<GameStateDTO> {
    const r = await fetch(`${API_BASE}/tictactoe/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!r.ok) throw new Error(`Create failed: ${r.status}`);
    return r.json();
  }

  async function playMove(index: number, player: Player): Promise<GameStateDTO> {
    if (!state) throw new Error("No game");
    const r = await fetch(`${API_BASE}/tictactoe/${state.id}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ index, player }),
    });
    if (!r.ok) {
      const detail = await r.json().catch(() => ({}));
      throw new Error(detail?.detail ?? `Move failed: ${r.status}`);
    }
    return r.json();
  }

  async function handleClick(i: number) {
    if (!state || loading || !isPlayable || disabled) return;
    // Light client-side guard to avoid noisy 400s:
    if (state.winner || state.is_draw || state.board[i] !== null) return;

    setLoading(true);
    setError(null);
    try {
      const next = await playMove(i, currentPlayer);
      setState(next);
      onMoveMade(i);
      switchPlayer(); // Switch player after every move
    } catch (e: any) {
      setError(e?.message ?? "Move failed");
    } finally {
      setLoading(false);
    }
  }

  async function reset() {
    setLoading(true);
    setError(null);
    try {
      const gs = await createGame();
      setState(gs);
    } catch (e: any) {
      setError(e?.message ?? "Failed to reset");
    } finally {
      setLoading(false);
    }
  }

  if (error) {
    return (
      <div className="max-w-sm mx-auto p-4">
        <div className="mb-2 text-red-600 font-semibold">Error: {error}</div>
        <button className="rounded-2xl px-4 py-2 border" onClick={reset}>
          Retry
        </button>
      </div>
    );
  }

  if (!state) {
    return (
      <div className="max-w-sm mx-auto p-4">
        <div className="text-center">Loading…</div>
      </div>
    );
  }

  const { board, status } = state;

  return (
    <div className={`w-full h-full relative ${!isPlayable ? 'opacity-50' : ''}`}>
      {/* Tic-tac-toe board lines - darker gray for sub-games */}
      <div className="absolute inset-0">
        {/* Horizontal lines */}
        <div className="absolute w-full h-0.5 bg-gray-500 top-1/3 left-0 transform -translate-y-0.25"></div>
        <div className="absolute w-full h-0.5 bg-gray-500 top-2/3 left-0 transform -translate-y-0.25"></div>
        {/* Vertical lines */}
        <div className="absolute h-full w-0.5 bg-gray-500 left-1/3 top-0 transform -translate-x-0.25"></div>
        <div className="absolute h-full w-0.5 bg-gray-500 left-2/3 top-0 transform -translate-x-0.25"></div>
      </div>
      {/* Game cells */}
      {board.map((c, i) => {
        const row = Math.floor(i / 3);
        const col = i % 3;
        return (
          <button
            key={i}
            className="absolute w-1/3 h-1/3 text-lg font-bold flex items-center justify-center disabled:opacity-50 hover:bg-gray-100"
            style={{
              top: `${row * 33.333}%`,
              left: `${col * 33.333}%`,
            }}
            onClick={() => handleClick(i)}
            aria-label={`cell-${i}`}
            disabled={loading || c !== null || state.winner !== null || state.is_draw || !isPlayable || disabled}
          >
            {c}
          </button>
        );
      })}
    </div>
  );
}