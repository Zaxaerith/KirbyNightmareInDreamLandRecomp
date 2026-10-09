# Required local inputs

Supply your own legally obtained **Kirby: Nightmare in Dream Land (USA), Rev 0** ROM.

| Field | Required value |
|---|---|
| Filename used locally | `Kirby - Nightmare in Dream Land (USA).gba` |
| Length | 8,388,608 bytes |
| Header | `AGB KIRBY DX` |
| Game code / revision | `A7KE` / `0` |
| SHA-1 | `37a476567d133c146fee6b5e2eb0b07a215da6b0` |

Real BIOS boot requires a user-supplied 16,384-byte GBA BIOS with SHA-1
`300c20df6731a33952ded8c436f7f186d25d3492`. Existing local input at
`../gbarecomp-cli-windows-x86_64/gbabios/gba_bios.bin` is reused without copying.
Override it with `-Bios <path>` in the scripts.

Scripts verify both inputs before regeneration or execution. ROMs, BIOS,
generated translations and saves must never be committed or distributed.
