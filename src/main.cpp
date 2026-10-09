#include "runtime.h"
#include <filesystem>
#include <string>
#include <vector>

int game_launcher_preboot(std::vector<std::string>&, const gbarecomp::RunOptions&);
int game_validate_inputs(std::vector<std::string>&, const gbarecomp::RunOptions&);

int main(int argc, char** argv) {
    gbarecomp::RunOptions options;
    options.builtin_game_name = "Kirby: Nightmare in Dream Land";
    options.builtin_rom_sha1 = "37a476567d133c146fee6b5e2eb0b07a215da6b0";
    options.launcher_region = "USA";
    options.launcher_game_config = "game.toml";
    options.launcher_expose_widescreen = false;
    options.launcher_expose_adaptive_view = false;
    options.launcher_save_path = "saves/kirby_nightmare_usa.sav";
    std::vector<std::string> args(argv, argv + argc);
    const bool player_launch = argc == 1 || (argc == 2 && args[1] == "--launcher");
    if (player_launch) {
        std::error_code error;
        auto exe = std::filesystem::absolute(argv[0], error);
        if (!error) std::filesystem::current_path(exe.parent_path(), error);
    }
    if (game_launcher_preboot(args, options)) return 0;
    if (game_validate_inputs(args, options)) return 1;
    if (player_launch) {
        args.emplace_back("--save");
        args.emplace_back(options.launcher_save_path);
        args.emplace_back("--window");
    }
    std::vector<char*> native_args;
    for (auto& arg : args) native_args.push_back(arg.data());
    return gbarecomp::run_game(static_cast<int>(native_args.size()), native_args.data(), options);
}
