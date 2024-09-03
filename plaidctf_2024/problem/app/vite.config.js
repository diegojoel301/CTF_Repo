import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
	plugins: [
		react(),
		{
			name: "setup-nonce",
			enforce: "post",
			transformIndexHtml(html) {
				return html.replace(
					/<(script |link [^>]*rel="stylesheet" )/g,
					`<$1nonce="NONCEPLACEHOLDER" `
				);
			}
		}
	],
	css: {
		modules: {
			localsConvention: "camelCaseOnly"
		}
	},
	resolve: {
		alias: {
			"@": "/src"
		}
	},
	define: {
		__DEV__: false
	},
	build: {
		outDir: "dist-ui"
	},
	server: {
		port: 3001,
		proxy: {
			"/api": {
				target: "http://127.0.0.1:3000",
				changeOrigin: true,
				secure: false
			}
		}
	}
});
