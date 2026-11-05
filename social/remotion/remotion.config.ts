import { Config } from "@remotion/cli/config";

// h264 + yuv420p + BT.709 keeps PY-Blauw on brand in every player.
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(95);
Config.setCodec("h264");
Config.setPixelFormat("yuv420p");
Config.setColorSpace("bt709");
Config.setCrf(16);
Config.setOverwriteOutput(true);
