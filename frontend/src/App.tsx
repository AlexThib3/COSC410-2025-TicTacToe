import React from "react";
import TicTacToe from "@/components/TicTacToe";
import { SuperTicTacToeProvider, useSuperTicTacToe } from "./SuperTicTacToeContext";

type Player = "X" | "O";
type SubGameResult = Player | "draw" | null;

function MainBoard() {
  const { mainBoard, currentPlayer, updateSubGame, switchPlayer, setNextLegalBoard, resetGame } = useSuperTicTacToe();
  const [mainWinner, setMainWinner] = React.useState<Player | "draw" | null>(null);

  React.useEffect(() => {
    // Check for main game winner
    const lines = [
      [0,1,2],[3,4,5],[6,7,8],
      [0,3,6],[1,4,7],[2,5,8],
      [0,4,8],[2,4,6],
    ];
    for (const [a, b, c] of lines) {
      if (mainBoard[a] && mainBoard[a] === mainBoard[b] && mainBoard[a] === mainBoard[c]) {
        setMainWinner(mainBoard[a] as Player);
        return;
      }
    }
    if (mainBoard.every(cell => cell !== null)) {
      setMainWinner("draw");
    }
  }, [mainBoard]);

  const handleSubGameEnd = (index: number, result: SubGameResult) => {
    updateSubGame(index, result);
  };

  const handleMoveMade = (cellIndex: number) => {
    setNextLegalBoard(cellIndex);
  };

  const handleReset = () => {
    setMainWinner(null);
    resetGame();
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="text-center mb-4 text-2xl font-bold">
        {mainWinner ? `${mainWinner === "draw" ? "Draw" : mainWinner + " wins the Super Game"}!` : `${currentPlayer}'s turn`}
      </div>
      <div className="relative w-full max-w-2xl mx-auto aspect-square mb-8">
        {/* Tic-tac-toe board lines - black for super board */}
        <div className="absolute inset-0">
          {/* Horizontal lines */}
          <div className="absolute w-full h-1 bg-black top-1/3 left-0 transform -translate-y-0.5"></div>
          <div className="absolute w-full h-1 bg-black top-2/3 left-0 transform -translate-y-0.5"></div>
          {/* Vertical lines */}
          <div className="absolute h-full w-1 bg-black left-1/3 top-0 transform -translate-x-0.5"></div>
          <div className="absolute h-full w-1 bg-black left-2/3 top-0 transform -translate-x-0.5"></div>
        </div>
        {/* Sub-games positioned in each cell */}
        {Array.from({ length: 9 }, (_, i) => {
          const row = Math.floor(i / 3);
          const col = i % 3;
          return (
            <div
              key={i}
              className="absolute w-1/4 h-1/4"
              style={{
                top: `${row * 33.333 + 4.166}%`,
                left: `${col * 33.333 + 4.166}%`,
              }}
            >
              <TicTacToe
                subGameIndex={i}
                onSubGameEnd={(result) => handleSubGameEnd(i, result)}
                onMoveMade={(cellIndex) => handleMoveMade(cellIndex)}
                disabled={!!mainWinner}
              />
              {/* Winner overlay for completed sub-games */}
              {mainBoard[i] && mainBoard[i] !== "draw" && (
                <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90">
                  <span className="text-6xl font-bold text-gray-800">
                    {mainBoard[i]}
                  </span>
                </div>
              )}
              {/* Draw overlay */}
              {mainBoard[i] === "draw" && (
                <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90">
                  <span className="text-2xl font-bold text-gray-600">
                    DRAW
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div className="text-center">
        <button
          className="rounded-2xl px-6 py-3 border-2 border-gray-400 hover:border-gray-600"
          onClick={handleReset}
        >
          New Super Game
        </button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <SuperTicTacToeProvider>
      <MainBoard />
    </SuperTicTacToeProvider>
  );
}
