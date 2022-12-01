import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    inventory_blobs = text_data.strip('\n').strip().split('\n\n')
    inventories = [[int(x) for x in blob.strip('\n').strip().split('\n')] for blob in inventory_blobs]
    return inventories

def get_top3_inventories(inventories):
    totals = [sum(inventory) for inventory in inventories]
    totals.sort(reverse=True)
    return sum(totals[0:3])

def get_max_inventory(inventories):
    totals = [sum(inventory) for inventory in inventories]
    return max(totals)

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    inventories = parse_data(data)
    answer = get_max_inventory(inventories)
    logger.info(f"Puzzle1: Largest Elf Inventory: {answer}")
    answer = get_top3_inventories(inventories)
    logger.info(f"Puzzle2: Sum of Top 3 Elf Inventories: {answer}")
    
if __name__ == '__main__':
    main()