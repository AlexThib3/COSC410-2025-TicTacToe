import React, { createContext, useContext, useState } from 'react';

type Player = "X" | "O";
type SubGameResult = Player | "draw" | null;

interface SuperTicTacToeContextType {
  currentPlayer: Player;
  legalBoards: number[];
  mainBoard: SubGameResult[];
  setMainBoard: React.Dispatch<React.SetStateAction<SubGameResult[]>>;
  updateSubGame: (index: number, result: SubGameResult) => void;
  switchPlayer: () => void;
  setNextLegalBoard: (board: number) => void;
  resetGame: () => void;
}

const SuperTicTacToeContext = createContext<SuperTicTacToeContextType | undefined>(undefined);

export const useSuperTicTacToe = () => {
  const context = useContext(SuperTicTacToeContext);
  if (!context) {
    throw new Error('useSuperTicTacToe must be used within SuperTicTacToeProvider');
  }
  return context;
};

interface ProviderProps {
  children: React.ReactNode;
}

export const SuperTicTacToeProvider: React.FC<ProviderProps> = ({ children }) => {
  const [currentPlayer, setCurrentPlayer] = useState<Player>("X");
  const [legalBoards, setLegalBoards] = useState<number[]>([0, 1, 2, 3, 4, 5, 6, 7, 8]);
  const [mainBoard, setMainBoard] = useState<SubGameResult[]>(Array(9).fill(null));

  const updateSubGame = (index: number, result: SubGameResult) => {
    setMainBoard(prev => {
      const next = [...prev];
      next[index] = result;
      return next;
    });
    setLegalBoards(prev => prev.filter(board => board !== index));
  };

  const setNextLegalBoard = (board: number) => {
    // After playing in sub-game N, next player must play in sub-game N, if available
    if (mainBoard[board] === null) {
      // Sub-game N is still active, so next player must play there
      setLegalBoards([board]);
    } else {
      // Sub-game N is finished (won/drawn), so all remaining sub-games are legal
      setLegalBoards([0, 1, 2, 3, 4, 5, 6, 7, 8].filter(b => mainBoard[b] === null));
    }
  };

  const switchPlayer = () => {
    setCurrentPlayer(prev => prev === "X" ? "O" : "X");
  };

  const resetGame = () => {
    setCurrentPlayer("X");
    setLegalBoards([0, 1, 2, 3, 4, 5, 6, 7, 8]);
    setMainBoard(Array(9).fill(null));
  };

  return (
    <SuperTicTacToeContext.Provider value={{
      currentPlayer,
      legalBoards,
      mainBoard,
      setMainBoard,
      updateSubGame,
      switchPlayer,
      setNextLegalBoard,
      resetGame,
    }}>
      {children}
    </SuperTicTacToeContext.Provider>
  );
};
