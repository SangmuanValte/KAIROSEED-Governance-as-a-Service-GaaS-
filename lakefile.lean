import Lake
open Lake DSL

package «kairoseed-verification» where
  version := v!"0.1.0"

@[default_target]
lean_lib «KairoseedVerification» where
  srcDir := "formal"
  roots := #[`verification]
