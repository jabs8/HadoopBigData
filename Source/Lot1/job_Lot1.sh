# Copier le fichier jar Hadoop Streaming dans le répertoire courant
cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
# Démarrer Hadoop
./start-hadoop.sh
# Démarrer HBase
start-hbase.sh
# Démarrer le service Thrift pour HBase
hbase-daemon.sh start thrift
# Créer le répertoire d'entrée dans HDFS s'il n'existe pas
hdfs dfs -mkdir -p input
# Charger le fichier CSV dans HDFS
hdfs dfs -put dataw_fro03.csv input
# Supprimer les anciens résultats dans HDFS, s'ils existent
hdfs dfs -rm -r outputjob_Lot1
# Exécuter le job Hadoop Streaming
hadoop jar hadoop-streaming-2.7.2.jar \
  -file mapper.py \
  -mapper "python3 mapper.py" \
  -file reducer.py \
  -reducer "python3 reducer.py" \
  -input input/dataw_fro03.csv \
  -output outputjob_Lot1

