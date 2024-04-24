#!/bin/bash
#SBATCH --job-name=persona
#SBATCH --output=persona.out
#SBATCH --error=persona.err
#SBATCH -N 1
#SBATCH -p general
#SBATCH --gres=gpu:A6000
#SBATCH --mem=32G
#SBATCH --time=0-08:00:00


echo "LOADING THE ENVIRONMENT"
source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate med
echo "Starting"

# Your job commands go here

persona_id=${1:-1}


python generate_personas.py "mmr" $persona_id > Generations/persona_$persona_id.txt

echo "DONE!!"
