# Site speaker
A minimal tool for transforming text content from the russian forums into speech
## Clone repo
```sh
git clone git@github.com/zeionara/site-speaker.git $HOME/site-speaker
cd $HOME/site-speaker
```
## Set up environment
```sh
conda create -f environment.yml
conda activate site-speaker
```
## Download some posts
```sh
python -m site_speaker read-many https://example.org/{i} -n 7 -o assets/txt/foo
```
## Generate speech
```sh
python -m site_speaker tts-many -i assets/txt/foo -s txt -o assets/mp3/foo -d mp3
```