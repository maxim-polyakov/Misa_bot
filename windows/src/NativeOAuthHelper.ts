import type { TurboModule } from "react-native";
import { TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
  getPendingOAuthUrl(): string | null;
  saveExportZipBase64(base64: string, fileName: string): Promise<string>;
}

export default TurboModuleRegistry.get<Spec>("OAuthHelper");
