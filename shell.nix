
with import <nixpkgs> {};
let
    pythonEnv = python313.withPackages(ps: [
        ps.python-dotenv
        ps.requests
        ps.mypy
        ps.pylint
        ps.pylsp-mypy
        ps.requests
    
    ]);
in
mkShell {
    packages = [
        pythonEnv
        streamlit

    ];
}