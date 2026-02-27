import { DarkMode, LightMode } from "@mui/icons-material";
import {
  createTheme,
  IconButton,
  Stack,
  ThemeProvider,
  Typography,
  useColorScheme,
} from "@mui/material";
import { useEffect, useState } from "react";
import { ReplayRow, fetchCSV } from "./readCsv";
import { ReplayDatagrid } from "./ReplayDatagrid";

// App component that fetches replay data and displays it in a datagrid
// with a toggle for light and dark themes.
function ReplayHolder({ allRows }: Readonly<{ allRows: ReplayRow[] }>) {
  if (allRows.length === 0) {
    return (
      <Typography variant="h6" sx={{ margin: 2 }}>
        Loading replays...
      </Typography>
    );
  } else {
    return <ReplayDatagrid allRows={allRows}></ReplayDatagrid>;
  }
}

export function App() {
  const { mode, setMode } = useColorScheme();
  const [rrows, setRrows] = useState([] as ReplayRow[]);

  useEffect(() => {
    fetchCSV("data.csv").then((rows) => setRrows(rows));
  }, []);

  const toggleTheme = () => {
    if (mode === "light") {
      setMode("dark");
      document.documentElement.classList.add("dark");
    } else {
      setMode("light");
      document.documentElement.classList.remove("dark");
    }
  };

  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      <Stack direction={"row"} spacing={2}>
        <Typography variant="h5">Pokemon Showdown Reborn Replay Server</Typography>

        <IconButton onClick={toggleTheme} aria-label="Toggle theme">
          {mode === "light" ? <LightMode /> : <DarkMode />}
        </IconButton>
      </Stack>
      <ReplayHolder allRows={rrows} />
    </div>
  );
}

const theme = createTheme({
  colorSchemes: {
    dark: true,
  },
});

export default function App2() {
  return (
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  );
}
