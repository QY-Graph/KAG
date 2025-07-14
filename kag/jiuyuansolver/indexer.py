import argparse
import os
import logging
import asyncio
from kag.common.registry import import_modules_from_path
from kag.builder.runner import BuilderChainRunner
from kag.jiuyuansolver.import_logs import LogsImporter
logger = logging.getLogger(__name__)

async def buildKB(file_path):
    from kag.common.conf import KAG_CONFIG
    runner = BuilderChainRunner.from_config(
        KAG_CONFIG.all_config["kag_builder_pipeline"]
    )
    await runner.ainvoke(file_path)
    logger.info(f"\n\nbuildKB successfully for {file_path}\n\n")

if __name__ == "__main__":
    import_modules_from_path(".")
    parser = argparse.ArgumentParser(description="args")
    parser.add_argument(
        "--corpus_file",
        type=str,
        help="test file name in /data",
        default="data/sub_corpus.json",
    )
    args = parser.parse_args()
    file_path = args.corpus_file
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, file_path)
    # 导入pg 构建向量数据库
    db_config = {
        "host": "localhost",
        "port": 5432,
        "user": "wr",
        "password": "your_password",
        "database": "test"
    }
    importer = LogsImporter(db_config)
    try:
        # 连接数据库
        importer.sync_connect()
        importer.db.sync_init_graph_tables()
    except Exception as e:
        logger.error(f"Error during import: {str(e)}")
    finally:
        # 关闭连接
        importer.sync_close()


    asyncio.run(buildKB(file_path))