import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    base: "./",
    build: {
        outDir: "../PokemonShowdown-Client/play.pokemonshowdown.com/replays",
        rollupOptions: {
            input: {
                client: 'testclient.html',
            },
            output: {
                manualChunks: {
                    react: ["react", "react-dom"],
                    mui: ["@mui/material", "@mui/icons-material"],
                    muidatagrid: ["@mui/x-data-grid"],
                },
            },
        },
    },
});
